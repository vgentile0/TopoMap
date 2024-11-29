from pyvis.network import Network
import os

def plot_network_and_route_with_pyvis(route_result, target, active_hosts, local_ip, domain=None):
    """
    Visualizza la rete interna e il traceroute verso il target usando pyvis.
    """
    # Creazione del grafo interattivo
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

    # Nodo locale (dispositivo corrente)
    local_label = f"Local IP: {local_ip}"
    net.add_node("Local", label=local_label, color="cyan", shape="box")

    # Identificazione del router (primo hop)
    router_label = None
    if route_result:
        router_label = f"Router: {route_result[0][1]}"
        net.add_node(router_label, label=route_result[0][1], color="purple", shape="ellipse")
        net.add_edge("Local", router_label)

    # Aggiunge gli host attivi
    for host in active_hosts:
        net.add_node(host, label=host, color="green", shape="dot")
        net.add_edge(router_label or "Local", host)

    # Aggiunge gli hop del traceroute
    hop_labels = []
    for idx, (snd, rcv) in enumerate(route_result):
        hop_label = f"Hop {idx + 1}: {rcv}"
        net.add_node(hop_label, label=rcv, color="orange", shape="ellipse")
        hop_labels.append(hop_label)

        # Collega gli hop in ordine
        if idx == 0:
            net.add_edge(router_label or "Local", hop_label)
        else:
            net.add_edge(hop_labels[idx - 1], hop_label)

    # Collega l'ultimo hop al Target
    target_label = f"{target} ({domain})" if domain else target
    net.add_node("Target", label=target_label, color="red", shape="star")
    if hop_labels:
        net.add_edge(hop_labels[-1], "Target")

    # Generazione del file HTML per il grafo
    output_file = os.path.join(os.getcwd(), "network_topology.html")
    net.show(output_file, notebook=False)  # Impostazione notebook=False
    print(f"Visualizzazione generata: {output_file}")
