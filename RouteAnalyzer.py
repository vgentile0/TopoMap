import networkx as nx
import matplotlib.pyplot as plt
import os

def plot_route(route_result, target, active_hosts):
    # Create an empty graph
    G = nx.DiGraph()  # Use direct graph

    # Add starting node
    G.add_node(0, label=target)  # Starting node (target)

    # Iteriamo attraverso i risultati di traceroute e aggiungiamo nodi e collegamenti
    for idx, (snd, rcv) in enumerate(route_result):
        G.add_node(idx + 1, label=rcv.src)  # Add node with index
        if idx > 0:
            # Add link from previous node to current one
            G.add_edge(idx, idx + 1)

    # Add Lan Host to starting node
    for host in active_hosts:
        # Aggiungi un nodo per ogni host attivo
        G.add_node(host, label=host)  # Nodo per l'host attivo
        G.add_edge(0, host)  # Collega l'host al nodo di partenza

    # Draw graph
    pos = nx.spring_layout(G)  # Layout: Spring
    plt.figure(figsize=(16, 12))  # Figure size set

    # Define node colours & dimensions
    node_colors = []
    node_sizes = []
    for node in G.nodes():
        if node == 0:  # Starting node
            node_colors.append("skyblue")  # Target Colour
            node_sizes.append(1000)  # Target Size
        elif node in active_hosts:  # Lan active host
            node_colors.append("green")  # green for lan host
            node_sizes.append(500)  # size of lan hosts nodes
        else:  # Nodi del traceroute
            node_colors.append("lightgray")  # Traceroute nodes colour
            node_sizes.append(800)  # Tracert Nodes size

    # Draw graph with defined rules
    nx.draw(G, pos, with_labels=True, node_size=node_sizes, node_color=node_colors, font_size=10, font_weight="bold", edge_color="gray")

    # Add node captures
    node_labels = {i: rcv.src for i, (snd, rcv) in enumerate(route_result)}
    node_labels.update({host: host for host in active_hosts})  # Add captures to lan hosts nodes
    nx.draw_networkx_labels(G, pos, labels=node_labels)

    # Modifica lo spessore dei rami
    edge_widths = [1 if node in active_hosts and G.nodes[node]['label'] != target else 2 for node in G.edges()]
    nx.draw_networkx_edges(G, pos, width=edge_widths)

    plt.title(f"Traceroute to {target} and Active Hosts")

    # Save plot in  Documents/TopoMap
    documents_path = os.path.expanduser("~/Documents/TopoMap")
    os.makedirs(documents_path, exist_ok=True)  # Create folder if does't exist
    plt.savefig(os.path.join(documents_path, 'traceroute_graph.png'))  # Save image

    plt.show()
