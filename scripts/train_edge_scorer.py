"""
Train the edge-scoring GNN on road-network TSP instances with supervised labels.

Pipeline:
1. Generate training data by solving small instances (50-100 stops) with best solver
2. Train GNN with binary cross-entropy on edge inclusion
3. Evaluate precision/recall on held-out validation set
4. Save model checkpoint
"""

import sys
import os
import json
import signal
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

from src.data_pipeline import generate_synthetic_road_network
from src.baselines import solve, tour_cost
from src.models.edge_scorer import EdgeScorerGNN, prepare_graph_data

# Timeout
class ComputeTimeout(Exception):
    pass

def _handler(signum, frame):
    raise ComputeTimeout()

signal.signal(signal.SIGALRM, _handler)

SEED = 42
torch.manual_seed(SEED)
np.random.seed(SEED)


class TSPGraphDataset(Dataset):
    """Dataset of solved TSP instances for edge-scoring training."""

    def __init__(self, instances: list):
        self.instances = instances

    def __len__(self):
        return len(self.instances)

    def __getitem__(self, idx):
        return self.instances[idx]


def generate_training_data(n_instances: int = 500, sizes=(50, 75, 100),
                           cities=("synthetic_manhattan", "synthetic_london", "synthetic_berlin"),
                           time_limit_s: float = 10.0) -> list:
    """Generate training instances by solving with best available solver."""
    instances = []
    total = 0

    for i in range(n_instances):
        if total % 50 == 0:
            print(f"  Generating instance {total}/{n_instances}...")

        n_stops = sizes[i % len(sizes)]
        city = cities[i % len(cities)]
        seed = SEED + i

        signal.alarm(60)  # 60s timeout per instance
        try:
            data = generate_synthetic_road_network(
                n_points=n_stops,
                city_name=city,
                seed=seed,
                area_km=7.0,
            )

            cost_mat = data["durations"]

            # Solve with OR-Tools (fast and reliable)
            tour, cost = solve(cost_mat, "ortools", time_limit_s=time_limit_s, seed=seed)

            # Also try lkh_style for small instances
            if n_stops <= 75:
                tour2, cost2 = solve(cost_mat, "lkh_style", time_limit_s=time_limit_s, seed=seed)
                if cost2 < cost:
                    tour, cost = tour2, cost2

            signal.alarm(0)

            # Prepare graph data with labels
            graph_data = prepare_graph_data(cost_mat, data["coordinates"], tour)
            instances.append(graph_data)
            total += 1

        except (ComputeTimeout, Exception) as e:
            signal.alarm(0)
            continue

    print(f"  Generated {len(instances)} training instances")
    return instances


def collate_graphs(batch):
    """Collate multiple graphs into a single batched graph."""
    node_feats = []
    edge_feats = []
    edge_index = []
    labels = []
    node_offset = 0

    for graph in batch:
        n = graph["node_feats"].shape[0]
        node_feats.append(graph["node_feats"])
        edge_feats.append(graph["edge_feats"])
        edge_index.append(graph["edge_index"] + node_offset)
        labels.append(graph["labels"])
        node_offset += n

    return {
        "node_feats": torch.cat(node_feats, dim=0),
        "edge_feats": torch.cat(edge_feats, dim=0),
        "edge_index": torch.cat(edge_index, dim=1),
        "labels": torch.cat(labels, dim=0),
    }


def train_model(train_data, val_data, n_epochs=30, lr=1e-3, batch_size=8,
                hidden_dim=64, n_layers=3):
    """Train the edge-scoring GNN."""
    model = EdgeScorerGNN(
        node_input_dim=4,
        edge_input_dim=4,
        hidden_dim=hidden_dim,
        n_layers=n_layers,
        n_heads=4,
        dropout=0.1,
    )

    # Compute class weights for imbalanced labels
    all_labels = torch.cat([d["labels"] for d in train_data])
    pos_count = all_labels.sum().item()
    neg_count = len(all_labels) - pos_count
    pos_weight = torch.tensor([neg_count / (pos_count + 1e-10)])
    print(f"  Positive samples: {pos_count:.0f}/{len(all_labels)} "
          f"({pos_count/len(all_labels)*100:.1f}%), pos_weight={pos_weight.item():.2f}")

    criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=1e-5)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=n_epochs)

    train_dataset = TSPGraphDataset(train_data)
    val_dataset = TSPGraphDataset(val_data)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True,
                              collate_fn=collate_graphs)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False,
                            collate_fn=collate_graphs)

    training_log = []
    best_val_f1 = 0
    best_model_state = None

    for epoch in range(n_epochs):
        # Training
        model.train()
        train_loss = 0
        n_batches = 0

        for batch in train_loader:
            optimizer.zero_grad()
            logits = model.get_logits(batch["node_feats"], batch["edge_feats"],
                                      batch["edge_index"])
            loss = criterion(logits, batch["labels"])
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            train_loss += loss.item()
            n_batches += 1

        scheduler.step()
        train_loss /= max(n_batches, 1)

        # Validation
        model.eval()
        val_loss = 0
        all_preds = []
        all_targets = []
        n_val_batches = 0

        with torch.no_grad():
            for batch in val_loader:
                logits = model.get_logits(batch["node_feats"], batch["edge_feats"],
                                          batch["edge_index"])
                loss = criterion(logits, batch["labels"])
                val_loss += loss.item()
                n_val_batches += 1

                preds = torch.sigmoid(logits) > 0.5
                all_preds.append(preds)
                all_targets.append(batch["labels"] > 0.5)

        val_loss /= max(n_val_batches, 1)
        all_preds = torch.cat(all_preds)
        all_targets = torch.cat(all_targets)

        tp = (all_preds & all_targets).sum().item()
        fp = (all_preds & ~all_targets).sum().item()
        fn = (~all_preds & all_targets).sum().item()

        precision = tp / (tp + fp + 1e-10)
        recall = tp / (tp + fn + 1e-10)
        f1 = 2 * precision * recall / (precision + recall + 1e-10)

        log_entry = {
            "epoch": epoch + 1,
            "train_loss": round(train_loss, 6),
            "val_loss": round(val_loss, 6),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
            "lr": round(scheduler.get_last_lr()[0], 8),
        }
        training_log.append(log_entry)

        if (epoch + 1) % 5 == 0 or epoch == 0:
            print(f"  Epoch {epoch+1:3d}: train_loss={train_loss:.4f} val_loss={val_loss:.4f} "
                  f"P={precision:.3f} R={recall:.3f} F1={f1:.3f}")

        if f1 > best_val_f1:
            best_val_f1 = f1
            best_model_state = {k: v.clone() for k, v in model.state_dict().items()}

    # Load best model
    if best_model_state:
        model.load_state_dict(best_model_state)

    return model, training_log


def main():
    print("=" * 60)
    print("Training Edge-Scoring GNN for Road-Network ATSP")
    print("=" * 60)

    # Generate training data
    print("\n1. Generating training data (500 instances)...")
    t0 = time.time()
    all_data = generate_training_data(n_instances=500, time_limit_s=5.0)
    gen_time = time.time() - t0
    print(f"   Data generation took {gen_time:.1f}s")

    if len(all_data) < 100:
        print(f"   WARNING: Only {len(all_data)} instances generated. Trying with simpler settings...")
        all_data = generate_training_data(n_instances=300, sizes=(50,), time_limit_s=3.0)

    # Split train/val (80/20)
    n_total = len(all_data)
    n_train = int(0.8 * n_total)
    np.random.shuffle(all_data)
    train_data = all_data[:n_train]
    val_data = all_data[n_train:]
    print(f"   Train: {len(train_data)}, Val: {len(val_data)}")

    # Train model
    print("\n2. Training model...")
    t0 = time.time()
    model, training_log = train_model(train_data, val_data, n_epochs=30, lr=1e-3, batch_size=8)
    train_time = time.time() - t0
    print(f"   Training took {train_time:.1f}s")

    # Report final metrics
    final = training_log[-1]
    best = max(training_log, key=lambda x: x["f1"])
    print(f"\n3. Results:")
    print(f"   Final: P={final['precision']:.3f} R={final['recall']:.3f} F1={final['f1']:.3f}")
    print(f"   Best:  P={best['precision']:.3f} R={best['recall']:.3f} F1={best['f1']:.3f} (epoch {best['epoch']})")

    # Save model
    os.makedirs("models", exist_ok=True)
    torch.save(model.state_dict(), "models/edge_scorer.pt")
    print(f"   Model saved to models/edge_scorer.pt")

    # Save training log
    os.makedirs("results", exist_ok=True)
    with open("results/training_log.json", "w") as f:
        json.dump(training_log, f, indent=2)

    # Also save as CSV
    import csv
    with open("results/training_log.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=training_log[0].keys())
        writer.writeheader()
        writer.writerows(training_log)

    print(f"   Training log saved to results/training_log.csv")

    return model, training_log


if __name__ == "__main__":
    main()
