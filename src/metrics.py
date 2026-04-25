import networkx as nx


def tree_arity(G):
    """
    Maximum number of children (out-degree) of any node.
    """
    if len(G.nodes) == 0:
        return 0

    return max(G.out_degree(n) for n in G.nodes)


def count_crossings(G):
    """
    Count crossing edges in a dependency tree.
    """

    edges = list(G.edges())
    crossings = 0

    for i in range(len(edges)):
        for j in range(i + 1, len(edges)):

            a, b = edges[i]
            c, d = edges[j]

            if a > b:
                a, b = b, a
            if c > d:
                c, d = d, c

            if (a < c < b < d) or (c < a < d < b):
                crossings += 1

    return crossings

def tree_depth(G):
    """
    Longest root-to-leaf path in the tree.
    """

    roots = [n for n, d in G.in_degree() if d == 0]

    if not roots:
        return 0

    root = roots[0]

    depths = {}

    def dfs(node, depth):
        depths[node] = depth
        for child in G.successors(node):
            dfs(child, depth + 1)

    dfs(root, 0)

    return max(depths.values())