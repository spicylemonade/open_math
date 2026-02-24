"""
Training pipeline for the GNN edge scorer model.

Generates training instances, solves them with OR-Tools to get labels,
and trains the GNN with supervised learning (binary cross-entropy).
"""

import os
import sys
import json
import time
import signal

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.data.instance_generator import generate_synthetic_instance
from src.baselines.ortools_baseline import solve_ortools
from src.baselines.construction_heuristics import solve_nearest_neighbor
from src.models.edge_scorer import AsymmetricEdgeScorer, build_edge_scorer


class ComputeTimeout(Exception):
    pass


def generate_training_data(n_instances=1000, min_nodes=20, max_nodes=50,
                           seed=42, time_limit_per_instance=5.0):
    """Generate training instances and solve them for labels.

    Returns list of (instance, solution_tour) pairs.
    """
    rng = np.random.RandomState(seed)
    data = []
    topologies = ["grid", "radial", "mixed"]

    for i in range(n_instances):
        n = rng.randint(min_nodes, max_nodes + 1)
        topo = topologies[i % 3]
        s = seed + i

        inst = generate_synthetic_instance(
            n, seed=s, city_name=f"train_{i}",
            topology=topo, asymmetry_level=0.15
        )

        # Solve with OR-Tools (fast, good quality)
        try:
            result = solve_ortools(inst, time_limit=time_limit_per_instance, seed=42)
            tour = result["tour"]
        except Exception:
            # Fall back to nearest neighbor
            result = solve_nearest_neighbor(inst, seed=42)
            tour = result["tour"]

        data.append((inst, tour))

        if (i + 1) % 100 == 0:
            print(f"  Generated {i + 1}/{n_instances} training instances")

    return data


def tour_to_edge_labels(tour, n_nodes):
    """Convert a tour to binary edge labels.

    Returns a dict mapping (i, j) -> 1 for edges in the tour.
    """
    labels = {}
    for k in range(len(tour)):
        i = tour[k]
        j = tour[(k + 1) % len(tour)]
        labels[(i, j)] = 1
    return labels


def train_model(model, train_data, val_data, n_epochs=30, lr=1e-3,
                batch_size=32, device='cpu', save_dir='models',
                figures_dir='figures'):
    """Train the GNN edge scorer.

    Parameters
    ----------
    model : AsymmetricEdgeScorer
    train_data : list of (instance, tour) pairs
    val_data : list of (instance, tour) pairs
    n_epochs : int
    lr : float
    batch_size : int
    device : str
    save_dir : str
    figures_dir : str

    Returns
    -------
    dict with training history
    """
    model = model.to(device)
    optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=1e-5)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=n_epochs)

    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)

    history = {
        'train_loss': [], 'val_loss': [],
        'val_precision': [], 'val_recall': [], 'val_f1': []
    }

    best_val_f1 = 0.0

    for epoch in range(n_epochs):
        # Training
        model.train()
        epoch_loss = 0.0
        n_batches = 0

        indices = np.random.permutation(len(train_data))

        for batch_start in range(0, len(train_data), batch_size):
            batch_idx = indices[batch_start:batch_start + batch_size]
            batch_loss = 0.0

            for idx in batch_idx:
                inst, tour = train_data[idx]
                n = inst['metadata']['n_nodes']

                # Get features
                node_feat, edge_feat, edge_index = \
                    AsymmetricEdgeScorer.instance_to_features(inst)
                node_feat = node_feat.to(device)
                edge_feat = edge_feat.to(device)
                edge_index = edge_index.to(device)

                # Get labels
                tour_edges = tour_to_edge_labels(tour, n)
                n_edges = edge_index.shape[1]
                labels = torch.zeros(n_edges, device=device)
                for e in range(n_edges):
                    src = edge_index[0, e].item()
                    dst = edge_index[1, e].item()
                    if (src, dst) in tour_edges:
                        labels[e] = 1.0

                # Forward
                scores = model(node_feat, edge_feat, edge_index)

                # Weighted BCE loss (tour edges are rare: n out of n*(n-1))
                pos_weight = torch.tensor([(n - 2)], device=device, dtype=torch.float32)
                loss = nn.functional.binary_cross_entropy(
                    scores, labels,
                    weight=(labels * (pos_weight - 1) + 1)
                )
                batch_loss += loss

            batch_loss = batch_loss / len(batch_idx)
            optimizer.zero_grad()
            batch_loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()

            epoch_loss += batch_loss.item()
            n_batches += 1

        scheduler.step()
        avg_train_loss = epoch_loss / max(n_batches, 1)

        # Validation
        val_metrics = evaluate_model(model, val_data, device)
        avg_val_loss = val_metrics['loss']

        history['train_loss'].append(avg_train_loss)
        history['val_loss'].append(avg_val_loss)
        history['val_precision'].append(val_metrics['precision'])
        history['val_recall'].append(val_metrics['recall'])
        history['val_f1'].append(val_metrics['f1'])

        print(f"  Epoch {epoch + 1}/{n_epochs}: "
              f"train_loss={avg_train_loss:.4f}, "
              f"val_loss={avg_val_loss:.4f}, "
              f"P={val_metrics['precision']:.3f}, "
              f"R={val_metrics['recall']:.3f}, "
              f"F1={val_metrics['f1']:.3f}")

        # Save best model
        if val_metrics['f1'] > best_val_f1:
            best_val_f1 = val_metrics['f1']
            torch.save(model.state_dict(), os.path.join(save_dir, 'edge_scorer_best.pt'))

    # Save final model
    torch.save(model.state_dict(), os.path.join(save_dir, 'edge_scorer_final.pt'))

    # Save training history
    with open(os.path.join(save_dir, 'training_history.json'), 'w') as f:
        json.dump(history, f, indent=2)

    return history


def evaluate_model(model, data, device='cpu'):
    """Evaluate model on a dataset. Returns metrics dict."""
    model.eval()
    total_loss = 0.0
    total_tp = 0
    total_fp = 0
    total_fn = 0
    n_samples = 0

    with torch.no_grad():
        for inst, tour in data:
            n = inst['metadata']['n_nodes']
            node_feat, edge_feat, edge_index = \
                AsymmetricEdgeScorer.instance_to_features(inst)
            node_feat = node_feat.to(device)
            edge_feat = edge_feat.to(device)
            edge_index = edge_index.to(device)

            tour_edges = tour_to_edge_labels(tour, n)
            n_edges = edge_index.shape[1]
            labels = torch.zeros(n_edges, device=device)
            for e in range(n_edges):
                src = edge_index[0, e].item()
                dst = edge_index[1, e].item()
                if (src, dst) in tour_edges:
                    labels[e] = 1.0

            scores = model(node_feat, edge_feat, edge_index)

            pos_weight = torch.tensor([(n - 2)], device=device, dtype=torch.float32)
            loss = nn.functional.binary_cross_entropy(
                scores, labels,
                weight=(labels * (pos_weight - 1) + 1)
            )
            total_loss += loss.item()

            # Metrics with threshold 0.5
            preds = (scores > 0.5).float()
            tp = ((preds == 1) & (labels == 1)).sum().item()
            fp = ((preds == 1) & (labels == 0)).sum().item()
            fn = ((preds == 0) & (labels == 1)).sum().item()

            total_tp += tp
            total_fp += fp
            total_fn += fn
            n_samples += 1

    precision = total_tp / max(total_tp + total_fp, 1)
    recall = total_tp / max(total_tp + total_fn, 1)
    f1 = 2 * precision * recall / max(precision + recall, 1e-8)

    return {
        'loss': total_loss / max(n_samples, 1),
        'precision': precision,
        'recall': recall,
        'f1': f1,
    }


def plot_training_curves(history, save_path):
    """Plot training loss and validation metrics."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import seaborn as sns

    sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
    import matplotlib as mpl
    mpl.rcParams.update({
        'figure.figsize': (8, 5), 'figure.dpi': 300,
        'axes.spines.top': False, 'axes.spines.right': False,
        'axes.linewidth': 0.8, 'axes.labelsize': 13,
        'axes.titlesize': 14, 'axes.titleweight': 'bold',
        'xtick.labelsize': 11, 'ytick.labelsize': 11,
        'legend.fontsize': 11, 'legend.framealpha': 0.9,
        'legend.edgecolor': '0.8', 'font.family': 'serif',
        'grid.alpha': 0.3, 'grid.linewidth': 0.5,
        'savefig.bbox': 'tight', 'savefig.pad_inches': 0.1,
    })

    colors = sns.color_palette("deep")
    epochs = range(1, len(history['train_loss']) + 1)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5),
                                    constrained_layout=True)

    # Loss curves
    ax1.plot(epochs, history['train_loss'], '-o', color=colors[0],
             markersize=3, label='Train Loss', linewidth=1.5)
    ax1.plot(epochs, history['val_loss'], '-s', color=colors[1],
             markersize=3, label='Val Loss', linewidth=1.5)
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss (weighted BCE)')
    ax1.set_title('Training and Validation Loss')
    ax1.legend(frameon=True)

    # Precision/Recall/F1
    ax2.plot(epochs, history['val_precision'], '-o', color=colors[2],
             markersize=3, label='Precision', linewidth=1.5)
    ax2.plot(epochs, history['val_recall'], '-s', color=colors[3],
             markersize=3, label='Recall', linewidth=1.5)
    ax2.plot(epochs, history['val_f1'], '-^', color=colors[4],
             markersize=3, label='F1 Score', linewidth=1.5)
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Score')
    ax2.set_title('Validation Metrics')
    ax2.set_ylim(0, 1.05)
    ax2.legend(frameon=True)

    plt.savefig(save_path.replace('.png', '.pdf'))
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"  Training curves saved to {save_path}")


if __name__ == "__main__":
    # Set timeout for entire training
    def timeout_handler(signum, frame):
        raise ComputeTimeout("Training timed out")

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(480)  # 8 minute total limit

    try:
        print("Step 1: Generating training data (1000 instances)...")
        train_data = generate_training_data(
            n_instances=1000, min_nodes=20, max_nodes=50,
            seed=42, time_limit_per_instance=3.0
        )

        print("Step 2: Generating validation data (200 instances)...")
        val_data = generate_training_data(
            n_instances=200, min_nodes=20, max_nodes=50,
            seed=12345, time_limit_per_instance=3.0
        )

        print("Step 3: Building model...")
        model = build_edge_scorer(hidden_dim=64, n_layers=3, dropout=0.1)
        print(f"  Parameters: {sum(p.numel() for p in model.parameters()):,}")

        print("Step 4: Training...")
        history = train_model(
            model, train_data, val_data,
            n_epochs=30, lr=1e-3, batch_size=16,
            device='cpu', save_dir='models', figures_dir='figures'
        )

        signal.alarm(0)

        print("\nStep 5: Plotting training curves...")
        plot_training_curves(history, 'figures/training_loss.png')

        # Final metrics
        final = {
            'precision': history['val_precision'][-1],
            'recall': history['val_recall'][-1],
            'f1': history['val_f1'][-1],
            'best_f1': max(history['val_f1']),
        }
        print(f"\nFinal: P={final['precision']:.3f}, "
              f"R={final['recall']:.3f}, F1={final['f1']:.3f}")
        print(f"Best F1: {final['best_f1']:.3f}")

    except ComputeTimeout:
        signal.alarm(0)
        print("Training timed out - saving partial results")
