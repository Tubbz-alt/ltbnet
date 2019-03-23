import networkx as nx
from matplotlib import pyplot as plt

import matplotlib.pyplot as plt
import networkx as nx
try:
    import pygraphviz
    from networkx.drawing.nx_agraph import graphviz_layout
except ImportError:
    try:
        import pydot
        from networkx.drawing.nx_pydot import graphviz_layout
    except ImportError:
        raise ImportError("This example needs Graphviz and either "
                          "PyGraphviz or pydot")


def make_graph(network):
    """Graph visualization of a Network object
    """
    G = nx.Graph()

    G.add_nodes_from(network.Switch.idx, color='red', size=200)
    G.add_nodes_from(network.PMU.idx, color='green', size=80)
    G.add_nodes_from(network.PDC.idx, color='blue', size=160)

    for f, t in zip(network.Link.fr, network.Link.to):
        G.add_edge(f, t)

    print("graph has %d nodes with %d edges"
          % (nx.number_of_nodes(G), nx.number_of_edges(G)))
    print(nx.number_connected_components(G), "connected components")

    colors = [G.node[i]['color'] for i in G.nodes()]
    sizes = [G.node[i]['size'] for i in G.nodes()]

    plt.figure(figsize=(8, 8))
    # use graphviz to find radial layout
    pos = graphviz_layout(G, prog='sfdp', root='S_CAIS')
    # draw nodes, coloring by rtt ping time
    nx.draw(G, pos,
            node_color=colors,
            with_labels=False,
            alpha=0.6,
            node_size=sizes
            )

    labels = {i: i for i in network.Switch.idx}

    nx.draw_networkx_labels(G, pos, labels, font_size=16, font_color='black')

    path = nx.shortest_path(G, source='C_AESO', target='C_SRP')

    print(path)
    path_edges = zip(path, path[1:])
    path_edges = list(path_edges)
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='r', node_size=240, alpha=0.5)
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=10, alpha=0.4)

    plt.show()

    return g