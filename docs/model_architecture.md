# GNN Edge Scorer Architecture

## Overview
We design an asymmetry-aware Graph Neural Network (GNN) for scoring directed edges in Asymmetric Traveling Salesman Problem (ATSP) instances. The model predicts the probability that each directed edge (i -> j) belongs to the optimal tour. These scores are used to guide local search heuristics by prioritizing promising candidate edges.

## Key Design Decisions

### 1. Directed Message Passing
Unlike standard GNN architectures that operate on undirected graphs, our model processes directed edges explicitly. For road network ATSP, c(i,j) != c(j,i) is the norm (one-way streets, different routes in each direction). The message passing respects edge directionality.

### 2. Asymmetry-Aware Edge Features
Each directed edge (i -> j) is encoded with features that capture both the forward and reverse cost:
- Forward cost c_ij (normalized by max cost in instance)
- Reverse cost c_ji
- Asymmetry ratio: c_ij / c_ji (captures degree of directional preference)
- Cost rank: rank of c_ij among all outgoing edges from i (normalized to [0,1])

### 3. Node Features
Each node is encoded with:
- Coordinates (lat, lon) if available, normalized to [0,1]
- Mean outgoing cost (normalized)
- Mean incoming cost (normalized)
- Out-degree cost variance
- In-degree cost variance
- Node index embedding (learned, for positional information)

## Architecture Details

### Input Processing
- Node encoder: Linear(node_dim, hidden_dim)
- Edge encoder: Linear(edge_dim, hidden_dim)

### Message Passing Stack (3 layers)
Each DirectedMessagePassingLayer:
1. Compute attention weights: alpha_ij = softmax(LeakyReLU(a^T [W*h_i || W*h_j || e_ij]))
2. Aggregate messages: m_i = sum_j(alpha_ij * W_msg * h_j)  (sum over in-neighbors)
3. Update: h_i' = ReLU(W_self * h_i + m_i) + h_i  (residual connection)
4. LayerNorm + Dropout

### Edge Scoring Head
For each directed edge (i -> j):
1. Concatenate: [h_i || h_j || e_ij]  (source, destination, edge features)
2. MLP: Linear(3*hidden_dim, hidden_dim) -> ReLU -> Dropout -> Linear(hidden_dim, 1)
3. Sigmoid activation -> probability in [0, 1]

### Training
- Loss: Binary cross-entropy on edge membership in near-optimal tours
- Labels: 1 if edge (i,j) is in the LKH/OR-Tools solution, 0 otherwise
- Optimizer: Adam with lr=1e-3
- Training set: 1000 small ATSP instances (20-50 nodes) with near-optimal solutions

## Model Parameters
- node_dim: 8 (input node features)
- edge_dim: 8 (input edge features)
- hidden_dim: 64
- n_layers: 3
- dropout: 0.1
- Total parameters: ~50K (lightweight for fast inference)

## Inference
Given a new ATSP instance:
1. Convert to graph representation with node/edge features
2. Forward pass through GNN (~10ms for 200 nodes on CPU)
3. Output: n*n matrix of edge probabilities
4. Use top-k scoring edges as candidate set for local search
