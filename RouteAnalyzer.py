import networkx as nx
import matplotlib.pyplot as plt
import os


def plot_route(route_result, target, active_hosts):
    # Create an empty directed graph
    G = nx.DiGraph()

    # Add starting node (target)
    G.add_node(0, label=target)  # Starting node (target)

    # Iterate through the traceroute results and add nodes and edges
    for idx, (snd, rcv) in enumerate(route_result):
        # Add node with index
        G.add_node(idx + 1, label=rcv.src if idx < len(route_result) - 1 else target)
        if idx > 0:
            # Add edge from previous node to current one
            G.add_edge(idx, idx + 1)

    # Add edge between the starting node (0) and the first traceroute node (1)
    if len(route_result) > 0:
        G.add_edge(0, 1)

    # Add LAN hosts and connect them to the starting node
    for host in active_hosts:
        G.add_node(host, label=host)  # Add node for each active host
        G.add_edge(0, host)  # Connect the host to the starting node

    # Draw the graph
    pos = nx.spring_layout(G)  # Layout: Spring
    plt.figure(figsize=(32, 24))  # Set figure size

    # Define node colors and sizes
    node_colors = []
    node_sizes = []
    for node in G.nodes():
        if node == 0:  # Starting node
            node_colors.append("skyblue")  # Color for target node
            node_sizes.append(1000)  # Size for target node
        elif node == len(route_result):  # Last traceroute node
            node_colors.append("orange")  # Orange for last traceroute node
            node_sizes.append(1000)  # Larger size for the last traceroute node
        elif node in active_hosts:  # LAN active hosts
            node_colors.append("green")  # Green for LAN hosts
            node_sizes.append(400)  # Smaller size for LAN hosts
        else:  # Traceroute nodes
            node_colors.append("blue")  # Color for other traceroute nodes
            node_sizes.append(800)  # Size for other traceroute nodes

    # Draw the graph with the predefined rules
    nx.draw(G, pos, with_labels=True, node_size=node_sizes, node_color=node_colors, font_size=8, font_weight="bold",
            edge_color="gray")

    # Add node labels
    node_labels = {i: rcv.src for i, (snd, rcv) in enumerate(route_result)}

    # Ensure the last traceroute node displays the target label
    if len(route_result) > 0:
        node_labels[len(route_result)] = target  # Set the last traceroute node's label to the target

    # Add labels for LAN hosts
    # node_labels.update({host: host for host in active_hosts})  #not necessary: duplicate label

    nx.draw_networkx_labels(G, pos, labels=node_labels)

    # Separate traceroute edges from LAN edges
    traceroute_edges = [(i, i + 1) for i in range(len(route_result))]  # Traceroute edges
    lan_edges = [(0, host) for host in active_hosts]  # LAN host edges

    # Draw traceroute edges in blue
    nx.draw_networkx_edges(G, pos, edgelist=traceroute_edges, edge_color='blue', width=2)

    # Draw LAN host edges in gray
    nx.draw_networkx_edges(G, pos, edgelist=lan_edges, edge_color='gray', width=1)

    plt.title(f"Traceroute to {target} and Active Hosts")

    # Save the plot in the Documents/TopoMap folder
    documents_path = os.path.expanduser("~/Documents/TopoMap")
    os.makedirs(documents_path, exist_ok=True)  # Create folder if it doesn't exist
    plt.savefig(os.path.join(documents_path, 'traceroute_graph.png'))  # Save the image

    plt.show()
