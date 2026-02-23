"""
Planar graph data structures, generators, and loaders.

Provides an adjacency-list Graph class, planarity testing, random planar
graph generators, and PACE .gr format file loading.
"""

import random
import math
from collections import defaultdict, deque
import networkx as nx


class Graph:
    """Adjacency-list graph supporting node/edge operations."""

    def __init__(self):
        self._adj = defaultdict(set)
        self._nodes = set()

    @property
    def nodes(self):
        return frozenset(self._nodes)

    @property
    def n(self):
        return len(self._nodes)

    @property
    def m(self):
        return sum(len(nb) for nb in self._adj.values()) // 2

    def add_node(self, v):
        self._nodes.add(v)

    def add_edge(self, u, v):
        if u == v:
            return
        self._nodes.add(u)
        self._nodes.add(v)
        self._adj[u].add(v)
        self._adj[v].add(u)

    def remove_edge(self, u, v):
        self._adj[u].discard(v)
        self._adj[v].discard(u)

    def remove_node(self, v):
        if v not in self._nodes:
            return
        for u in list(self._adj[v]):
            self._adj[u].discard(v)
        del self._adj[v]
        self._nodes.discard(v)

    def neighbors(self, v):
        return frozenset(self._adj[v])

    def closed_neighbors(self, v):
        return self._adj[v] | {v}

    def degree(self, v):
        return len(self._adj[v])

    def has_edge(self, u, v):
        return v in self._adj[u]

    def has_node(self, v):
        return v in self._nodes

    def edges(self):
        seen = set()
        for u in self._nodes:
            for v in self._adj[u]:
                if (v, u) not in seen:
                    seen.add((u, v))
                    yield (u, v)

    def subgraph(self, node_set):
        sg = Graph()
        node_set = set(node_set)
        for v in node_set:
            sg.add_node(v)
        for u in node_set:
            for v in self._adj[u]:
                if v in node_set and v > u:
                    sg.add_edge(u, v)
        return sg

    def to_networkx(self):
        G = nx.Graph()
        G.add_nodes_from(self._nodes)
        G.add_edges_from(self.edges())
        return G

    @staticmethod
    def from_networkx(nxG):
        g = Graph()
        for v in nxG.nodes():
            g.add_node(v)
        for u, v in nxG.edges():
            g.add_edge(u, v)
        return g

    def connected_components(self):
        visited = set()
        components = []
        for start in self._nodes:
            if start in visited:
                continue
            comp = set()
            queue = deque([start])
            while queue:
                v = queue.popleft()
                if v in comp:
                    continue
                comp.add(v)
                visited.add(v)
                for u in self._adj[v]:
                    if u not in comp:
                        queue.append(u)
            components.append(comp)
        return components

    def bfs_layers(self, source):
        layers = []
        visited = {source}
        current = [source]
        while current:
            layers.append(current)
            next_layer = []
            for v in current:
                for u in self._adj[v]:
                    if u not in visited:
                        visited.add(u)
                        next_layer.append(u)
            current = next_layer
        return layers

    def is_dominating_set(self, D):
        D = set(D)
        dominated = set(D)
        for v in D:
            dominated |= self._adj[v]
        return self._nodes <= dominated

    def copy(self):
        g = Graph()
        g._nodes = set(self._nodes)
        g._adj = defaultdict(set)
        for v in self._adj:
            g._adj[v] = set(self._adj[v])
        return g


def is_planar(g):
    """Test planarity using NetworkX Boyer-Myrvold."""
    nxG = g.to_networkx()
    return nx.check_planarity(nxG)[0]


def generate_grid_graph(rows, cols):
    """Generate a planar grid graph with rows x cols vertices."""
    g = Graph()
    for r in range(rows):
        for c in range(cols):
            v = r * cols + c
            g.add_node(v)
            if c > 0:
                g.add_edge(v, v - 1)
            if r > 0:
                g.add_edge(v, v - cols)
    return g


def generate_random_planar_graph(n, seed=42):
    """Generate a random planar graph efficiently.

    Uses Delaunay triangulation as a maximally planar graph, then randomly
    removes a fraction of edges to produce a sparser planar graph.
    This is always fast and always produces a planar graph.
    """
    rng = random.Random(seed)
    if n <= 3:
        g = Graph()
        nodes = list(range(n))
        for v in nodes:
            g.add_node(v)
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                g.add_edge(nodes[i], nodes[j])
        return g

    # Generate Delaunay triangulation (always planar, fast)
    import numpy as np
    np.random.seed(seed)
    try:
        from scipy.spatial import Delaunay
        points = np.random.rand(n, 2)
        tri = Delaunay(points)
        all_edges = set()
        for simplex in tri.simplices:
            for i in range(3):
                for j in range(i + 1, 3):
                    u, v = int(simplex[i]), int(simplex[j])
                    all_edges.add((min(u, v), max(u, v)))

        # Build full Delaunay graph first (guaranteed planar)
        nxG_full = nx.Graph()
        nxG_full.add_nodes_from(range(n))
        nxG_full.add_edges_from(all_edges)

        # Get a spanning tree to guarantee connectivity
        tree_edges = set()
        for u, v in nx.bfs_edges(nxG_full, 0):
            tree_edges.add((min(u, v), max(u, v)))

        # Non-tree edges that we can randomly include/exclude
        non_tree = list(all_edges - tree_edges)
        rng.shuffle(non_tree)
        # Keep ~50% of non-tree edges
        keep = int(len(non_tree) * 0.5)
        kept_non_tree = non_tree[:keep]

        g = Graph()
        for i in range(n):
            g.add_node(i)
        for u, v in tree_edges:
            g.add_edge(u, v)
        for u, v in kept_non_tree:
            g.add_edge(u, v)

        return g
    except ImportError:
        nxG = nx.random_labeled_tree(n)
        g = Graph.from_networkx(nxG)
        return g


def generate_delaunay_planar_graph(n, seed=42):
    """Generate a planar graph from Delaunay triangulation of random points."""
    rng = random.Random(seed)
    try:
        from scipy.spatial import Delaunay
        import numpy as np
        np.random.seed(seed)
        points = np.random.rand(n, 2)
        tri = Delaunay(points)
        g = Graph()
        for i in range(n):
            g.add_node(i)
        for simplex in tri.simplices:
            for i in range(3):
                for j in range(i + 1, 3):
                    g.add_edge(int(simplex[i]), int(simplex[j]))
        return g
    except ImportError:
        # Fallback to random planar
        return generate_random_planar_graph(n, seed)


def generate_triangulated_planar_graph(n, seed=42):
    """Generate a maximal planar (triangulated) graph.

    Uses Delaunay triangulation for n >= 4, producing a graph with
    close to 3n - 6 edges.
    """
    return generate_delaunay_planar_graph(n, seed)


def generate_path_graph(n):
    """Generate a path graph P_n."""
    g = Graph()
    for i in range(n):
        g.add_node(i)
        if i > 0:
            g.add_edge(i - 1, i)
    return g


def generate_cycle_graph(n):
    """Generate a cycle graph C_n."""
    g = Graph()
    for i in range(n):
        g.add_node(i)
        g.add_edge(i, (i + 1) % n)
    return g


def load_pace_format(filepath):
    """Load a graph from PACE .gr format.

    Format:
      c comment lines
      p ds <n> <m>
      <u> <v>   (1-indexed edges)
    """
    g = Graph()
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('c'):
                continue
            if line.startswith('p'):
                parts = line.split()
                n = int(parts[2])
                for i in range(1, n + 1):
                    g.add_node(i)
            else:
                parts = line.split()
                if len(parts) >= 2:
                    u, v = int(parts[0]), int(parts[1])
                    g.add_edge(u, v)
    return g


def save_pace_format(g, filepath):
    """Save a graph in PACE .gr format (1-indexed)."""
    node_map = {v: i + 1 for i, v in enumerate(sorted(g.nodes))}
    with open(filepath, 'w') as f:
        f.write(f"p ds {g.n} {g.m}\n")
        for u, v in g.edges():
            f.write(f"{node_map[u]} {node_map[v]}\n")
