import networkx as nx
import matplotlib.pyplot as plt
from main import subnetHost


def build_network_graph(devices, routes):
    G = nx.Graph()

    # Aggiungere i nodi (dispositivi)
    for device in devices:
        G.add_node(device['ip'], label=device['mac'])

    # Aggiungere gli archi (rotte)
    for route in routes:
        G.add_edge(route[0], route[1])

    # Disegnare il grafo
    nx.draw(G, with_labels=True)
    plt.show()


# Supponiamo che "devices" e "routes" siano ottenuti tramite le scansioni precedenti
#routes = [('192.168.1.1', '192.168.1.10'), ('192.168.1.1', '192.168.1.20')]
#build_network_graph(devices, routes)
