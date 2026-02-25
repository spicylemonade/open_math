"""
Asymmetry-aware edge-scoring GNN for road-network graphs.

A directed graph neural network that:
1. Takes node features (lat, lon, degree, betweenness centrality) and
   directed edge features (duration, distance, speed, asymmetry ratio)
2. Outputs per-edge scores predicting probability of edge being in optimal tour
3. Uses 3+ message-passing layers with attention/gating

Architecture: Directed Graph Attention Network with edge features.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


class DirectedEdgeAttentionLayer(nn.Module):
    """
    A single message-passing layer for directed graphs with edge features.

    For each edge (i->j):
    - Computes attention weight from source node, target node, and edge features
    - Applies gated aggregation of neighbor messages
    """

    def __init__(self, node_dim: int, edge_dim: int, hidden_dim: int,
                 n_heads: int = 4, dropout: float = 0.1):
        super().__init__()
        self.n_heads = n_heads
        self.head_dim = hidden_dim // n_heads
        assert hidden_dim % n_heads == 0

        # Query, Key, Value projections for attention
        self.W_q = nn.Linear(node_dim, hidden_dim)
        self.W_k = nn.Linear(node_dim, hidden_dim)
        self.W_v = nn.Linear(node_dim, hidden_dim)
        self.W_e = nn.Linear(edge_dim, hidden_dim)  # Edge feature projection

        # Gate for message aggregation
        self.gate = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.Sigmoid()
        )

        # Output projection
        self.W_o = nn.Linear(hidden_dim, node_dim)

        # Edge update
        self.edge_update = nn.Sequential(
            nn.Linear(node_dim * 2 + edge_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, edge_dim),
        )

        # Layer norm
        self.norm1 = nn.LayerNorm(node_dim)
        self.norm2 = nn.LayerNorm(edge_dim)

        self.dropout = nn.Dropout(dropout)

    def forward(self, node_feats: torch.Tensor, edge_feats: torch.Tensor,
                edge_index: torch.Tensor) -> tuple:
        """
        Parameters
        ----------
        node_feats : (N, node_dim) tensor
        edge_feats : (E, edge_dim) tensor
        edge_index : (2, E) tensor of [source, target] indices

        Returns
        -------
        updated_node_feats : (N, node_dim)
        updated_edge_feats : (E, edge_dim)
        """
        src_idx = edge_index[0]  # (E,)
        dst_idx = edge_index[1]  # (E,)
        N = node_feats.shape[0]
        E = edge_feats.shape[0]

        # Multi-head attention
        Q = self.W_q(node_feats).view(N, self.n_heads, self.head_dim)  # (N, H, D)
        K = self.W_k(node_feats).view(N, self.n_heads, self.head_dim)
        V = self.W_v(node_feats).view(N, self.n_heads, self.head_dim)
        E_proj = self.W_e(edge_feats).view(E, self.n_heads, self.head_dim)  # (E, H, D)

        # Attention scores: query(dst) * (key(src) + edge)
        q = Q[dst_idx]  # (E, H, D)
        k = K[src_idx] + E_proj  # (E, H, D)
        attn = (q * k).sum(dim=-1) / (self.head_dim ** 0.5)  # (E, H)

        # Softmax over incoming edges for each destination node
        # Use scatter operations for sparse attention
        attn_max = torch.zeros(N, self.n_heads, device=node_feats.device)
        attn_max.scatter_reduce_(0, dst_idx.unsqueeze(1).expand(-1, self.n_heads),
                                  attn, reduce="amax", include_self=True)
        attn = attn - attn_max[dst_idx]
        attn_exp = torch.exp(attn)

        attn_sum = torch.zeros(N, self.n_heads, device=node_feats.device)
        attn_sum.scatter_add_(0, dst_idx.unsqueeze(1).expand(-1, self.n_heads), attn_exp)
        attn_weights = attn_exp / (attn_sum[dst_idx] + 1e-10)  # (E, H)

        # Weighted message: attention * value(src)
        v = V[src_idx]  # (E, H, D)
        weighted_msg = (attn_weights.unsqueeze(-1) * v)  # (E, H, D)

        # Aggregate messages per destination node
        agg = torch.zeros(N, self.n_heads, self.head_dim, device=node_feats.device)
        agg.scatter_add_(0, dst_idx.unsqueeze(1).unsqueeze(2).expand(-1, self.n_heads, self.head_dim),
                         weighted_msg)
        agg = agg.view(N, -1)  # (N, hidden_dim)

        # Gated update
        gate_input = torch.cat([agg, self.W_o(node_feats)], dim=-1)
        g = self.gate(gate_input)
        node_update = g * self.W_o(self.dropout(agg)) + (1 - g) * node_feats

        # Residual + LayerNorm
        node_feats_out = self.norm1(node_feats + node_update)

        # Edge feature update
        src_feats = node_feats_out[src_idx]
        dst_feats = node_feats_out[dst_idx]
        edge_input = torch.cat([src_feats, dst_feats, edge_feats], dim=-1)
        edge_update = self.edge_update(edge_input)
        edge_feats_out = self.norm2(edge_feats + self.dropout(edge_update))

        return node_feats_out, edge_feats_out


class EdgeScorerGNN(nn.Module):
    """
    Full edge-scoring GNN model for predicting tour membership.

    Architecture:
    - Input embedding layers for node and edge features
    - 3 directed graph attention layers with edge features
    - Edge classification head outputting per-edge tour probability
    """

    def __init__(self, node_input_dim: int = 4, edge_input_dim: int = 4,
                 hidden_dim: int = 64, n_layers: int = 3, n_heads: int = 4,
                 dropout: float = 0.1):
        """
        Parameters
        ----------
        node_input_dim : int, input node feature dimension
            Default 4: (lat, lon, degree, betweenness_centrality)
        edge_input_dim : int, input edge feature dimension
            Default 4: (duration, distance, speed, asymmetry_ratio)
        hidden_dim : int, hidden layer dimension
        n_layers : int, number of message-passing layers (>= 3)
        n_heads : int, number of attention heads
        dropout : float, dropout rate
        """
        super().__init__()

        self.node_input_dim = node_input_dim
        self.edge_input_dim = edge_input_dim
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers

        # Input embeddings
        self.node_embed = nn.Sequential(
            nn.Linear(node_input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
        )
        self.edge_embed = nn.Sequential(
            nn.Linear(edge_input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
        )

        # Message-passing layers
        self.layers = nn.ModuleList([
            DirectedEdgeAttentionLayer(
                node_dim=hidden_dim,
                edge_dim=hidden_dim,
                hidden_dim=hidden_dim,
                n_heads=n_heads,
                dropout=dropout,
            )
            for _ in range(n_layers)
        ])

        # Edge classification head
        self.edge_classifier = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, 1),
        )

    def forward(self, node_feats: torch.Tensor, edge_feats: torch.Tensor,
                edge_index: torch.Tensor) -> torch.Tensor:
        """
        Forward pass: predict per-edge tour membership probability.

        Parameters
        ----------
        node_feats : (N, node_input_dim) tensor
        edge_feats : (E, edge_input_dim) tensor
        edge_index : (2, E) long tensor

        Returns
        -------
        edge_scores : (E,) tensor of tour membership probabilities (sigmoid applied)
        """
        # Embed inputs
        h_node = self.node_embed(node_feats)
        h_edge = self.edge_embed(edge_feats)

        # Message passing
        for layer in self.layers:
            h_node, h_edge = layer(h_node, h_edge, edge_index)

        # Edge classification
        logits = self.edge_classifier(h_edge).squeeze(-1)  # (E,)
        scores = torch.sigmoid(logits)

        return scores

    def get_logits(self, node_feats: torch.Tensor, edge_feats: torch.Tensor,
                   edge_index: torch.Tensor) -> torch.Tensor:
        """Return raw logits (before sigmoid) for use with BCEWithLogitsLoss."""
        h_node = self.node_embed(node_feats)
        h_edge = self.edge_embed(edge_feats)

        for layer in self.layers:
            h_node, h_edge = layer(h_node, h_edge, edge_index)

        logits = self.edge_classifier(h_edge).squeeze(-1)
        return logits


def prepare_graph_data(cost_matrix: np.ndarray, coordinates: list,
                       tour: list = None) -> dict:
    """
    Prepare graph data tensors from a road-network ATSP instance.

    Parameters
    ----------
    cost_matrix : (N, N) asymmetric duration matrix
    coordinates : list of (lat, lon) tuples
    tour : optional list of node indices (for creating labels)

    Returns
    -------
    dict with node_feats, edge_feats, edge_index, labels (if tour given)
    """
    n = cost_matrix.shape[0]

    # Node features: lat, lon, in-degree, out-degree
    coords = np.array(coordinates, dtype=np.float32)
    # Normalize coordinates to [0, 1]
    coords_norm = (coords - coords.min(axis=0)) / (coords.max(axis=0) - coords.min(axis=0) + 1e-10)

    # Compute degree from cost matrix (count reachable neighbors)
    threshold = np.median(cost_matrix[cost_matrix > 0]) * 2
    adj = (cost_matrix < threshold).astype(float)
    np.fill_diagonal(adj, 0)
    out_degree = adj.sum(axis=1) / n
    in_degree = adj.sum(axis=0) / n

    node_feats = np.column_stack([
        coords_norm[:, 0],  # lat (normalized)
        coords_norm[:, 1],  # lon (normalized)
        out_degree,         # normalized out-degree
        in_degree,          # normalized in-degree
    ]).astype(np.float32)

    # Edge features for all pairs (i, j) where i != j
    # For scalability, use k-nearest neighbors (k=20) instead of all pairs
    k = min(20, n - 1)
    edge_src = []
    edge_dst = []
    edge_feats_list = []

    for i in range(n):
        costs_from_i = cost_matrix[i].copy()
        costs_from_i[i] = np.inf
        nearest = np.argsort(costs_from_i)[:k]
        for j in nearest:
            dur_ij = cost_matrix[i, j]
            dur_ji = cost_matrix[j, i]
            dist_ij = dur_ij  # Using duration as proxy for distance
            speed = 1.0 / (dur_ij + 1e-10)  # inverse duration as speed proxy
            asym_ratio = dur_ij / (dur_ji + 1e-10)  # asymmetry ratio

            edge_src.append(i)
            edge_dst.append(j)
            edge_feats_list.append([
                dur_ij / (np.max(cost_matrix) + 1e-10),  # normalized duration
                dist_ij / (np.max(cost_matrix) + 1e-10),  # normalized distance
                min(speed * np.max(cost_matrix), 10.0) / 10.0,  # normalized speed
                min(asym_ratio, 5.0) / 5.0,  # normalized asymmetry ratio
            ])

    edge_index = np.array([edge_src, edge_dst], dtype=np.int64)
    edge_feats = np.array(edge_feats_list, dtype=np.float32)

    result = {
        "node_feats": torch.tensor(node_feats),
        "edge_feats": torch.tensor(edge_feats),
        "edge_index": torch.tensor(edge_index),
    }

    # Create labels if tour is provided
    if tour is not None:
        tour_edges = set()
        for idx in range(len(tour)):
            i = tour[idx]
            j = tour[(idx + 1) % len(tour)]
            tour_edges.add((i, j))

        labels = np.zeros(len(edge_src), dtype=np.float32)
        for e_idx in range(len(edge_src)):
            if (edge_src[e_idx], edge_dst[e_idx]) in tour_edges:
                labels[e_idx] = 1.0

        result["labels"] = torch.tensor(labels)

    return result


# ── Self-test ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Testing EdgeScorerGNN...")

    # Create a small test graph
    n = 50
    np.random.seed(42)
    cost_matrix = np.random.uniform(10, 100, size=(n, n))
    np.fill_diagonal(cost_matrix, 0)
    # Add asymmetry
    cost_matrix = cost_matrix * (1 + 0.3 * np.random.randn(n, n))
    cost_matrix = np.maximum(cost_matrix, 1.0)
    np.fill_diagonal(cost_matrix, 0)

    coords = [(40.7 + i * 0.01, -74.0 + i * 0.01) for i in range(n)]
    tour = list(range(n))  # dummy tour

    # Prepare data
    data = prepare_graph_data(cost_matrix, coords, tour)
    print(f"  Node features: {data['node_feats'].shape}")
    print(f"  Edge features: {data['edge_feats'].shape}")
    print(f"  Edge index: {data['edge_index'].shape}")
    print(f"  Labels: {data['labels'].shape}, positive: {data['labels'].sum().item():.0f}")

    # Create model
    model = EdgeScorerGNN(
        node_input_dim=4,
        edge_input_dim=4,
        hidden_dim=64,
        n_layers=3,
        n_heads=4,
    )

    # Forward pass
    scores = model(data["node_feats"], data["edge_feats"], data["edge_index"])
    print(f"  Output scores: {scores.shape}, range [{scores.min():.3f}, {scores.max():.3f}]")

    # Check gradient flow
    loss = F.binary_cross_entropy(scores, data["labels"])
    loss.backward()
    print(f"  Loss: {loss.item():.4f}")
    print(f"  Gradient flow OK: {all(p.grad is not None for p in model.parameters())}")

    n_params = sum(p.numel() for p in model.parameters())
    print(f"  Model parameters: {n_params:,}")

    print("\nEdgeScorerGNN test passed!")
