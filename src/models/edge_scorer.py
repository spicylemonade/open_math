"""
Asymmetry-aware Graph Neural Network for scoring directed edges in ATSP instances.

Architecture overview:
  - Node features: normalized coordinates + in/out degree cost statistics
  - Edge features: directed cost, reverse cost, asymmetry ratio, outgoing cost rank
  - 3 layers of directed message passing with attention weighted by edge features
  - Edge scoring MLP: concat(src_emb, dst_emb, edge_feat) -> 2-layer MLP -> sigmoid

This module depends only on PyTorch (no torch_geometric).
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


class DirectedMessagePassingLayer(nn.Module):
    """Single layer of directed message passing with edge-feature-aware attention.

    For each directed edge (i -> j) with edge embedding e_ij, compute:
        score_ij = LeakyReLU(a^T [W_q h_i || W_k h_j || W_e e_ij])
        alpha_ij = softmax_j(score_ij)   (over incoming neighbours of i)
        h_i'     = ReLU(W_self h_i + sum_j alpha_ij * W_msg h_j)

    Parameters
    ----------
    node_dim : int
        Dimensionality of node embeddings.
    edge_dim : int
        Dimensionality of edge embeddings.
    dropout : float
        Dropout probability applied to attention weights.
    """

    def __init__(self, node_dim, edge_dim, dropout=0.1):
        super().__init__()
        self.node_dim = node_dim
        self.edge_dim = edge_dim

        # Linear projections for attention computation
        self.W_q = nn.Linear(node_dim, node_dim, bias=False)
        self.W_k = nn.Linear(node_dim, node_dim, bias=False)
        self.W_e = nn.Linear(edge_dim, node_dim, bias=False)
        # Attention vector that maps concatenated projections to a scalar
        self.attn_vec = nn.Linear(3 * node_dim, 1, bias=False)

        # Node update transforms
        self.W_self = nn.Linear(node_dim, node_dim)
        self.W_msg = nn.Linear(node_dim, node_dim, bias=False)

        # Edge embedding update (optional, keeps edge info flowing)
        self.edge_update = nn.Linear(2 * node_dim + edge_dim, edge_dim)

        self.leaky_relu = nn.LeakyReLU(0.2)
        self.dropout = nn.Dropout(dropout)
        self.layer_norm = nn.LayerNorm(node_dim)

    def forward(self, h, e, edge_index):
        """
        Parameters
        ----------
        h : torch.Tensor, shape (n_nodes, node_dim)
            Current node embeddings.
        e : torch.Tensor, shape (n_edges, edge_dim)
            Current edge embeddings.
        edge_index : torch.Tensor, shape (2, n_edges)
            Directed edges as [src, dst] pairs.

        Returns
        -------
        h_new : torch.Tensor, shape (n_nodes, node_dim)
            Updated node embeddings.
        e_new : torch.Tensor, shape (n_edges, edge_dim)
            Updated edge embeddings.
        """
        src, dst = edge_index[0], edge_index[1]  # src -> dst
        n_nodes = h.size(0)
        n_edges = edge_index.size(1)

        # --- Attention computation ---
        q = self.W_q(h[dst])          # (n_edges, node_dim) -- destination queries
        k = self.W_k(h[src])          # (n_edges, node_dim) -- source keys
        e_proj = self.W_e(e)          # (n_edges, node_dim)
        attn_input = torch.cat([q, k, e_proj], dim=-1)  # (n_edges, 3*node_dim)
        attn_logits = self.attn_vec(self.leaky_relu(attn_input)).squeeze(-1)  # (n_edges,)

        # Softmax over incoming edges for each destination node
        attn_weights = self._sparse_softmax(attn_logits, dst, n_nodes)  # (n_edges,)
        attn_weights = self.dropout(attn_weights)

        # --- Message aggregation ---
        messages = self.W_msg(h[src])                     # (n_edges, node_dim)
        weighted_messages = attn_weights.unsqueeze(-1) * messages  # (n_edges, node_dim)

        # Scatter-add messages to destination nodes
        agg = torch.zeros(n_nodes, self.node_dim, device=h.device, dtype=h.dtype)
        agg.scatter_add_(0, dst.unsqueeze(-1).expand_as(weighted_messages), weighted_messages)

        # --- Node update with residual ---
        h_new = F.relu(self.W_self(h) + agg)
        h_new = self.layer_norm(h_new + h)  # residual connection

        # --- Edge embedding update ---
        e_new = self.edge_update(torch.cat([h_new[src], h_new[dst], e], dim=-1))
        e_new = F.relu(e_new) + e  # residual for edge embeddings

        return h_new, e_new

    @staticmethod
    def _sparse_softmax(logits, index, n_nodes):
        """Numerically stable softmax grouped by *index* (destination node).

        Parameters
        ----------
        logits : torch.Tensor, shape (n_edges,)
        index : torch.Tensor, shape (n_edges,)  -- destination node ids
        n_nodes : int

        Returns
        -------
        weights : torch.Tensor, shape (n_edges,)
        """
        # Compute per-group max for numerical stability
        max_vals = torch.full((n_nodes,), -1e9, device=logits.device, dtype=logits.dtype)
        max_vals.scatter_reduce_(0, index, logits, reduce='amax', include_self=True)
        logits_stable = logits - max_vals[index]

        exp_logits = torch.exp(logits_stable)

        # Sum of exps per destination node
        sum_exp = torch.zeros(n_nodes, device=logits.device, dtype=logits.dtype)
        sum_exp.scatter_add_(0, index, exp_logits)

        # Normalize
        weights = exp_logits / (sum_exp[index] + 1e-12)
        return weights


class AsymmetricEdgeScorer(nn.Module):
    """GNN model for scoring directed edges in ATSP instances.

    The model encodes an ATSP instance as a fully-connected directed graph
    (excluding self-loops) and predicts, for every directed edge, the
    probability that it belongs to the optimal tour.

    Parameters
    ----------
    node_dim : int
        Raw node feature dimensionality (before encoding).
    edge_dim : int
        Raw edge feature dimensionality (before encoding).
    hidden_dim : int
        Hidden dimensionality used throughout the network.
    n_layers : int
        Number of directed message-passing layers.
    dropout : float
        Dropout probability.
    """

    def __init__(self, node_dim=8, edge_dim=8, hidden_dim=64, n_layers=3, dropout=0.1):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers

        # ---------- Encoders ----------
        self.node_encoder = nn.Sequential(
            nn.Linear(node_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
        )
        self.edge_encoder = nn.Sequential(
            nn.Linear(edge_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
        )

        # ---------- Message-passing stack ----------
        self.mp_layers = nn.ModuleList([
            DirectedMessagePassingLayer(hidden_dim, hidden_dim, dropout=dropout)
            for _ in range(n_layers)
        ])

        # ---------- Edge scoring decoder ----------
        # Input: concat(src_emb, dst_emb, edge_emb) -> scalar probability
        self.edge_mlp = nn.Sequential(
            nn.Linear(3 * hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, 1),
        )

    def forward(self, node_features, edge_features, edge_index):
        """Run a forward pass and return per-edge scores.

        Parameters
        ----------
        node_features : torch.Tensor, shape (n_nodes, node_feat_dim)
            Raw node features (coordinates + degree statistics).
        edge_features : torch.Tensor, shape (n_edges, edge_feat_dim)
            Raw edge features (cost, reverse cost, asymmetry, rank, ...).
        edge_index : torch.Tensor, shape (2, n_edges)
            Directed edge list as [src, dst].

        Returns
        -------
        edge_scores : torch.Tensor, shape (n_edges,)
            Probability in [0, 1] that each directed edge is in the optimal tour.
        """
        # Encode raw features into hidden space
        h = self.node_encoder(node_features)   # (n_nodes, hidden_dim)
        e = self.edge_encoder(edge_features)   # (n_edges, hidden_dim)

        # Message passing
        for layer in self.mp_layers:
            h, e = layer(h, e, edge_index)

        # Decode edge scores
        src, dst = edge_index[0], edge_index[1]
        edge_repr = torch.cat([h[src], h[dst], e], dim=-1)  # (n_edges, 3*hidden_dim)
        edge_scores = torch.sigmoid(self.edge_mlp(edge_repr).squeeze(-1))  # (n_edges,)
        return edge_scores

    # ------------------------------------------------------------------
    # Instance conversion utility
    # ------------------------------------------------------------------
    @staticmethod
    def instance_to_features(instance, device=None):
        """Convert an ATSP instance dict to model input tensors.

        The instance dict is expected to follow the format produced by
        ``src.data.instance_generator``:
            - ``cost_matrix``: list-of-lists or 2-D array, shape (n, n)
            - ``coordinates``: list of (lat, lon) or (x, y) pairs (optional)

        Node features (dim = 8):
            0-1 : normalised x, y coordinates (zero-filled if absent)
              2 : mean outgoing cost (normalised)
              3 : mean incoming cost (normalised)
              4 : min outgoing cost (normalised)
              5 : min incoming cost (normalised)
              6 : std of outgoing costs (normalised)
              7 : std of incoming costs (normalised)

        Edge features (dim = 8):
            0 : normalised directed cost c_ij
            1 : normalised reverse cost c_ji
            2 : asymmetry ratio c_ij / c_ji  (clipped)
            3 : log asymmetry ratio  log(c_ij / c_ji)
            4 : rank of c_ij among outgoing edges of i (normalised to [0,1])
            5 : rank of c_ji among outgoing edges of j (normalised to [0,1])
            6 : normalised cost difference (c_ij - c_ji) / (c_ij + c_ji + eps)
            7 : indicator: 1 if c_ij < c_ji, else 0

        Parameters
        ----------
        instance : dict
            ATSP instance dictionary.
        device : torch.device or None
            Target device for the returned tensors.

        Returns
        -------
        node_features : torch.Tensor, shape (n, 8)
        edge_features : torch.Tensor, shape (n*(n-1), 8)
        edge_index : torch.Tensor, shape (2, n*(n-1))
        """
        cost_matrix = np.asarray(instance["cost_matrix"], dtype=np.float64)
        n = cost_matrix.shape[0]

        # ---------- Coordinate features ----------
        coords = np.zeros((n, 2), dtype=np.float64)
        if "coordinates" in instance and instance["coordinates"] is not None:
            raw_coords = np.asarray(instance["coordinates"], dtype=np.float64)
            if raw_coords.shape == (n, 2):
                coords = raw_coords.copy()

        # Normalise coordinates to [0, 1]
        for dim in range(2):
            cmin, cmax = coords[:, dim].min(), coords[:, dim].max()
            span = cmax - cmin
            if span > 1e-12:
                coords[:, dim] = (coords[:, dim] - cmin) / span

        # ---------- Cost statistics for node features ----------
        # Mask out diagonal (self-loops carry zero cost)
        mask = ~np.eye(n, dtype=bool)
        cost_no_diag = np.where(mask, cost_matrix, np.nan)

        # Global normalisation factor
        cost_max = np.nanmax(cost_no_diag) if np.any(mask) else 1.0
        cost_max = max(cost_max, 1e-12)
        normed_cost = cost_no_diag / cost_max

        out_mean = np.nanmean(normed_cost, axis=1)   # mean outgoing
        in_mean  = np.nanmean(normed_cost, axis=0)   # mean incoming
        out_min  = np.nanmin(normed_cost, axis=1)
        in_min   = np.nanmin(normed_cost, axis=0)
        out_std  = np.nanstd(normed_cost, axis=1)
        in_std   = np.nanstd(normed_cost, axis=0)

        node_feats = np.column_stack([
            coords[:, 0],   # 0: x
            coords[:, 1],   # 1: y
            out_mean,        # 2
            in_mean,         # 3
            out_min,         # 4
            in_min,          # 5
            out_std,         # 6
            in_std,          # 7
        ]).astype(np.float32)

        # ---------- Build directed edge list (all pairs, no self-loops) ----------
        src_ids = []
        dst_ids = []
        for i in range(n):
            for j in range(n):
                if i != j:
                    src_ids.append(i)
                    dst_ids.append(j)
        src_ids = np.array(src_ids, dtype=np.int64)
        dst_ids = np.array(dst_ids, dtype=np.int64)
        n_edges = len(src_ids)

        # ---------- Edge features ----------
        c_ij = cost_matrix[src_ids, dst_ids]           # directed cost
        c_ji = cost_matrix[dst_ids, src_ids]           # reverse cost

        # Normalise costs
        c_ij_norm = c_ij / cost_max
        c_ji_norm = c_ji / cost_max

        # Asymmetry ratio (clipped to avoid extreme values)
        eps = 1e-12
        asym_ratio = np.clip(c_ij / (c_ji + eps), 0.01, 100.0)
        log_asym = np.log(asym_ratio)

        # Outgoing rank: for each source node i, rank c_ij among its outgoing edges
        out_rank = np.zeros(n_edges, dtype=np.float32)
        # Incoming rank from reverse perspective
        rev_rank = np.zeros(n_edges, dtype=np.float32)

        for i in range(n):
            # Outgoing edges from node i
            out_mask = src_ids == i
            out_costs = c_ij[out_mask]
            ranks = np.argsort(np.argsort(out_costs)).astype(np.float32)
            if len(ranks) > 1:
                ranks /= (len(ranks) - 1)  # normalise to [0, 1]
            out_rank[out_mask] = ranks

            # Outgoing edges from node i in the reverse direction (for c_ji rank)
            dst_mask = dst_ids == i
            rev_costs = c_ji[dst_mask]
            rev_ranks = np.argsort(np.argsort(rev_costs)).astype(np.float32)
            if len(rev_ranks) > 1:
                rev_ranks /= (len(rev_ranks) - 1)
            rev_rank[dst_mask] = rev_ranks

        # Normalised cost difference
        cost_diff_norm = (c_ij - c_ji) / (c_ij + c_ji + eps)

        # Indicator: cheaper in forward direction
        cheaper_forward = (c_ij < c_ji).astype(np.float32)

        edge_feats = np.column_stack([
            c_ij_norm,        # 0: normalised forward cost
            c_ji_norm,        # 1: normalised reverse cost
            asym_ratio.clip(0, 5.0) / 5.0,  # 2: clipped & scaled asymmetry ratio
            np.clip(log_asym, -3, 3) / 3.0,  # 3: scaled log asymmetry
            out_rank,         # 4: outgoing cost rank
            rev_rank,         # 5: reverse cost rank
            cost_diff_norm,   # 6: normalised cost difference
            cheaper_forward,  # 7: indicator
        ]).astype(np.float32)

        # ---------- Convert to tensors ----------
        node_features = torch.from_numpy(node_feats)
        edge_features = torch.from_numpy(edge_feats)
        edge_index = torch.from_numpy(
            np.stack([src_ids, dst_ids], axis=0)
        )

        if device is not None:
            node_features = node_features.to(device)
            edge_features = edge_features.to(device)
            edge_index = edge_index.to(device)

        return node_features, edge_features, edge_index


# ---------------------------------------------------------------------------
# Convenience helpers
# ---------------------------------------------------------------------------

def build_edge_scorer(hidden_dim=64, n_layers=3, dropout=0.1):
    """Construct an AsymmetricEdgeScorer with default feature dimensions.

    The default feature dimensions (node_dim=8, edge_dim=8) match those
    produced by ``AsymmetricEdgeScorer.instance_to_features``.

    Parameters
    ----------
    hidden_dim : int
    n_layers : int
    dropout : float

    Returns
    -------
    AsymmetricEdgeScorer
    """
    return AsymmetricEdgeScorer(
        node_dim=8,
        edge_dim=8,
        hidden_dim=hidden_dim,
        n_layers=n_layers,
        dropout=dropout,
    )


def score_instance(model, instance, device=None):
    """Score all directed edges of an ATSP instance.

    Parameters
    ----------
    model : AsymmetricEdgeScorer
    instance : dict
        ATSP instance dictionary.
    device : torch.device or None

    Returns
    -------
    score_matrix : np.ndarray, shape (n, n)
        Matrix of edge scores; diagonal is zero.
    """
    model.eval()
    node_features, edge_features, edge_index = (
        AsymmetricEdgeScorer.instance_to_features(instance, device=device)
    )

    with torch.no_grad():
        scores = model(node_features, edge_features, edge_index)

    n = instance["metadata"]["n_nodes"] if "metadata" in instance else int(
        np.sqrt(edge_index.size(1) + 1) + 0.5
    )
    score_matrix = np.zeros((n, n), dtype=np.float64)
    src = edge_index[0].cpu().numpy()
    dst = edge_index[1].cpu().numpy()
    score_matrix[src, dst] = scores.cpu().numpy()
    return score_matrix
