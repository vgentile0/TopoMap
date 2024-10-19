import networkx as nx
import matplotlib.pyplot as plt
import os

def plot_route(route_result, target, active_hosts):
    # Creiamo un grafo vuoto
    G = nx.DiGraph()  # Utilizziamo un grafo diretto

    # Aggiungiamo il nodo di partenza
    G.add_node(0, label=target)  # Nodo di partenza (target)

    # Iteriamo attraverso i risultati di traceroute e aggiungiamo nodi e collegamenti
    for idx, (snd, rcv) in enumerate(route_result):
        G.add_node(idx + 1, label=rcv.src)  # Aggiungiamo un nodo con l'indice
        if idx > 0:
            # Aggiungiamo un collegamento dal nodo precedente a quello corrente
            G.add_edge(idx, idx + 1)

    # Aggiungi i dispositivi attivi come nodi attorno al primo nodo
    for host in active_hosts:
        # Aggiungi un nodo per ogni host attivo
        G.add_node(host, label=host)  # Nodo per l'host attivo
        G.add_edge(0, host)  # Collega l'host al nodo di partenza

    # Disegniamo il grafo
    pos = nx.spring_layout(G)  # Utilizziamo un layout spring
    plt.figure(figsize=(16, 12))  # Aumenta la dimensione della figura

    # Definisci i colori e le dimensioni per i nodi
    node_colors = []
    node_sizes = []
    for node in G.nodes():
        if node == 0:  # Nodo di partenza
            node_colors.append("skyblue")  # Colore per il nodo target
            node_sizes.append(1000)  # Dimensione grande per il nodo target
        elif node in active_hosts:  # Nodi attivi della LAN
            node_colors.append("green")  # Colore verde per i nodi della LAN
            node_sizes.append(500)  # Dimensione più piccola per i nodi attivi
        else:  # Nodi del traceroute
            node_colors.append("lightgray")  # Colore per i nodi del traceroute
            node_sizes.append(800)  # Dimensione media per i nodi del traceroute

    # Disegna il grafo con i colori e le dimensioni definiti
    nx.draw(G, pos, with_labels=True, node_size=node_sizes, node_color=node_colors, font_size=10, font_weight="bold", edge_color="gray")

    # Aggiungiamo le etichette sui nodi
    node_labels = {i: rcv.src for i, (snd, rcv) in enumerate(route_result)}
    node_labels.update({host: host for host in active_hosts})  # Aggiungi le etichette degli host attivi
    nx.draw_networkx_labels(G, pos, labels=node_labels)

    # Modifica lo spessore dei rami
    edge_widths = [1 if node in active_hosts and G.nodes[node]['label'] != target else 2 for node in G.edges()]
    nx.draw_networkx_edges(G, pos, width=edge_widths)

    plt.title(f"Traceroute to {target} and Active Hosts")

    # Salvataggio grafo nella cartella Documenti/TopoMap
    documents_path = os.path.expanduser("~/Documents/TopoMap")  # Percorso della cartella Documenti/TopoMap
    os.makedirs(documents_path, exist_ok=True)  # Crea la directory se non esiste
    plt.savefig(os.path.join(documents_path, 'traceroute_graph.png'))  # Salva l'immagine

    plt.show()
