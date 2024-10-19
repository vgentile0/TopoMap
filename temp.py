import networkx as nx
import matplotlib.pyplot as plt
import os

def plot_route(route_result, target):
    # Creiamo un grafo vuoto
    G = nx.DiGraph()  # Utilizziamo un grafo diretto

    # Iteriamo attraverso i risultati di traceroute e aggiungiamo nodi e collegamenti
    for idx, (snd, rcv) in enumerate(route_result):
        G.add_node(idx, label=rcv.src)  # Aggiungiamo un nodo con l'indice
        if idx > 0:
            # Aggiungiamo un collegamento dal nodo precedente a quello corrente
            G.add_edge(idx - 1, idx)

    # Disegniamo il grafo
    pos = nx.spring_layout(G)  # Utilizziamo un layout spring
    plt.figure(figsize=(12, 8))  # Dimensione della figura
    nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=10, font_weight="bold", edge_color="gray")

    # Aggiungiamo le etichette sui nodi
    node_labels = {i: rcv.src for i, (snd, rcv) in enumerate(route_result)}
    nx.draw_networkx_labels(G, pos, labels=node_labels)

    plt.title(f"Traceroute to {target}")

    # salvataggio grafo nella cartella Documenti/TopoMap
    documents_path = os.path.expanduser("~/Documents/TopoMap")  # Percorso della cartella Documenti/TopoMap
    os.makedirs(documents_path, exist_ok=True)  # Crea la directory se non esiste
    plt.savefig(os.path.join(documents_path, 'traceroute_graph.png'))  # Salva l'immagine

    plt.show()