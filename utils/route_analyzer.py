from pyvis.network import Network
import os

# Percorsi delle directory
RESULTS_FOLDER = "risultati_scansioni"
LOCAL_SCAN_FOLDER = os.path.join(RESULTS_FOLDER, "scansione_rete_locale")
TRACEROUTE_FOLDER = os.path.join(RESULTS_FOLDER, "traceroute")


def create_results_directories():
    """
    Crea le directory necessarie per memorizzare i risultati.
    """
    os.makedirs(LOCAL_SCAN_FOLDER, exist_ok=True)
    os.makedirs(TRACEROUTE_FOLDER, exist_ok=True)


def get_next_scan_number(folder):
    """
    Trova il prossimo numero di scansione incrementale per la rete locale.
    """
    files = os.listdir(folder)
    scans = [int(f.split("_")[1].split(".")[0]) for f in files if f.startswith("scansione_") and f.endswith(".html")]
    return max(scans, default=0) + 1


def save_local_network(active_hosts, local_ip, router_ip=None):
    """
    Visualizza e salva una rappresentazione grafica della rete locale.
    """
    # Crea il grafo
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

    # Nodo del router
    router_label = "Router" if not router_ip else f"Router: {router_ip}"
    net.add_node(router_label, label=router_label, color="purple", shape="ellipse")

    # Nodo locale (dispositivo corrente)
    local_label = f"Local IP: {local_ip}"
    net.add_node("Local", label=local_label, color="cyan", shape="box")
    net.add_edge(router_label, "Local")

    # Aggiunge gli host attivi
    for host in active_hosts:
        net.add_node(host, label=host, color="green", shape="dot")
        net.add_edge(router_label, host)

    # Salvataggio del file HTML
    scan_number = get_next_scan_number(LOCAL_SCAN_FOLDER)
    output_file = os.path.join(LOCAL_SCAN_FOLDER, f"scansione_{scan_number}.html")
    net.save_graph(output_file)

    print(f"Rappresentazione della rete locale salvata in: {output_file}")


def save_traceroute_result(route_result, target, active_hosts, local_ip, domain):
    """
    Visualizza e salva una rappresentazione grafica del traceroute.
    """
    # Crea il grafo
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
        hop_ip = rcv if isinstance(rcv, str) else rcv.src  # Usa solo l'IP
        net.add_node(hop_ip, label=hop_ip, color="orange", shape="ellipse")  # Usa l'IP come etichetta
        hop_labels.append(hop_ip)

        # Collega gli hop in ordine
        if idx == 0:
            net.add_edge(router_label or "Local", hop_ip)
        else:
            net.add_edge(hop_labels[idx - 1], hop_ip)

    # Collega l'ultimo hop al Target
    target_label = f"{target} ({domain})" if domain else target
    net.add_node("Target", label=target_label, color="red", shape="star")
    if hop_labels:
        net.add_edge(hop_labels[-1], "Target")

    # Salvataggio del file HTML
    output_file = os.path.join(TRACEROUTE_FOLDER, f"traceroute_{domain}.html")
    net.save_graph(output_file)

    print(f"Rappresentazione del traceroute salvata in: {output_file}")


