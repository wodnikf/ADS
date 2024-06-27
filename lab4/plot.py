import matplotlib.pyplot as plt
import networkx as nx

def build_graph(node, G, parent=None):
    if node is not None:
        if node.character is not None:
            label = f"{node.character} ({node.frequency})"
        else:
            label = f"Internal Node ({node.frequency})"
        G.add_node(label)
        if parent is not None:
            G.add_edge(parent, label)
        build_graph(node.left, G, label)
        build_graph(node.right, G, label)


def hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    if not nx.is_tree(G):
        raise TypeError('pos cannot be computed because G is not a tree.')

    def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None, parsed=[]):
        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)
        if len(children) != 0:
            dx = width / len(children)
            nextx = xcenter - width / 2 - dx / 2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                     vert_loc=vert_loc - vert_gap, xcenter=nextx, pos=pos, parent=root, parsed=parsed)
        return pos

    return _hierarchy_pos(G, root, width=1., vert_gap=vert_gap, vert_loc=vert_loc, xcenter=xcenter)


def draw_huffman_tree(root_node):
    G = nx.DiGraph()
    build_graph(root_node, G)
    
    pos = hierarchy_pos(G, list(G.nodes())[0])

    node_labels = {node: node for node in G.nodes()}

    nx.draw(G, pos, with_labels=True, labels=node_labels,
            node_color='skyblue', node_size=1500, edge_color='black',
            linewidths=1, font_size=12)

    plt.title('Huffman Tree')
    plt.savefig("Tree.png")
   # plt.show()