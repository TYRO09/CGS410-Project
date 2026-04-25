import random
import networkx as nx
from src.metrics import count_crossings


def generate_random_tree(n):
    """
    Generate a random labeled tree using Prüfer code.
    """
    if n <= 1:
        G = nx.DiGraph()
        G.add_node(1)
        return G

    prufer = [random.randint(1, n) for _ in range(n - 2)]

    degree = {i: 1 for i in range(1, n + 1)}
    for node in prufer:
        degree[node] += 1

    edges = []

    for node in prufer:
        for i in range(1, n + 1):
            if degree[i] == 1:
                edges.append((node, i))
                degree[node] -= 1
                degree[i] -= 1
                break

    remaining = [i for i in degree if degree[i] == 1]
    edges.append((remaining[0], remaining[1]))

    G = nx.DiGraph()
    for u, v in edges:
        G.add_edge(u, v)

    return G


def generate_random_tree_with_crossings(n, target_crossings, max_attempts=1000):
    """
    Generate a random tree whose crossing count matches the target.
    Uses rejection sampling with a retry cap to avoid infinite loops.
    """

    for _ in range(max_attempts):

        G = generate_random_tree(n)

        if count_crossings(G) == target_crossings:
            return G

    # fallback: return closest match if exact match not found
    best_tree = None
    best_diff = float("inf")

    for _ in range(100):

        G = generate_random_tree(n)
        diff = abs(count_crossings(G) - target_crossings)

        if diff < best_diff:
            best_tree = G
            best_diff = diff

            if diff == 0:
                break

    return best_tree