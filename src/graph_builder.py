import networkx as nx


def build_dependency_graph(sentence):
    """
    Convert a parsed sentence into a directed dependency graph.
    Nodes = word indices
    Edges = head → dependent
    """
    G = nx.DiGraph()

    for token in sentence:
        idx = token["id"]
        head = token["head"]

        G.add_node(idx)

        if head is not None and head != 0:  # 0 = root, None = unset
            G.add_edge(head, idx)

    return G