from pyvis.network import Network
# network di pyvis è una libreria che permette di creare grafi con nodi e archi che rappresentano una rete.
import os

# Percorsi delle directory
RESULTS_FOLDER = "risultati_scansioni"
LOCAL_SCAN_FOLDER = os.path.join(RESULTS_FOLDER, "scansione_rete_locale")
TRACEROUTE_FOLDER = os.path.join(RESULTS_FOLDER, "traceroute")

WORKING_DIR = "img"
ROUTER_IMAGE = os.path.join(WORKING_DIR, "router.png")
HOST_IMAGE = os.path.join(WORKING_DIR, "host.png")
TARGET_IMAGE = os.path.join(WORKING_DIR, "target.png")

router_image_path = os.path.abspath(ROUTER_IMAGE)
host_image_path = os.path.abspath(HOST_IMAGE)
target_image_path = os.path.abspath(TARGET_IMAGE)

# Debug per verificare l'esistenza delle immagini
# print(os.path.exists(ROUTER_IMAGE)) 
# print(os.path.exists(HOST_IMAGE))      

def create_results_directories():
    """
    Crea le directory necessarie per memorizzare i risultati delle scansioni.
    """
    os.makedirs(LOCAL_SCAN_FOLDER, exist_ok=True)
    os.makedirs(TRACEROUTE_FOLDER, exist_ok=True)


def get_next_scan_number(folder):
    """
    Definisce il numero della prossima scansione da salvare.
    """
    files = os.listdir(folder)
    scans = [int(f.split("_")[1].split(".")[0]) for f in files if f.startswith("scansione_") and f.endswith(".html")]
    return max(scans, default=0) + 1


def save_local_network(active_hosts, local_ip, router_ip=None):
    """
    Visualizza e salva una rappresentazione grafica della rete locale con il router al centro.
    """
    
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

    router_label = "Router" if not router_ip else f"Router: {router_ip}"
    net.add_node(
        "Router",
        label=router_label,
        shape="image",
        image=router_image_path,
        physics=False,  
        x=0,
        y=0
    )

    
    local_label = f"Local IP: {local_ip}"
    net.add_node("Local", label=local_label, shape="image", image=host_image_path)
    net.add_edge("Router", "Local")  

    
    for host in active_hosts:
        host_label = f"Host: {host}"
        net.add_node(host, label=host_label, shape="image", image=host_image_path)
        net.add_edge("Router", host)  

    # Salvataggio del file HTML
    scan_number = get_next_scan_number(LOCAL_SCAN_FOLDER)
    output_file = os.path.join(LOCAL_SCAN_FOLDER, f"scansione_{scan_number}.html")
    net.save_graph(output_file)

    print(f"Rappresentazione della rete locale salvata in: {output_file}")


def save_traceroute_result(route_result, target, active_hosts, local_ip, domain):
    """
    Visualizza e salva una rappresentazione grafica del traceroute.
    """
    
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

    
    local_label = f"Local IP: {local_ip}"
    net.add_node("Local", label=local_label, shape="image", image=host_image_path)

    router_label = None
    if route_result:
        router_label = f"Router: {route_result[0][1]}"
        net.add_node(router_label, label=route_result[0][1], shape="image", image=router_image_path)
        net.add_edge("Local", router_label)

    for host in active_hosts:
        net.add_node(host, label=host, shape="image", image=host_image_path)
        net.add_edge(router_label or "Local", host)

    hop_labels = []
    for idx, (snd, rcv) in enumerate(route_result):
        hop_ip = rcv if isinstance(rcv, str) else rcv.src  
        net.add_node(hop_ip, label=hop_ip, shape="image", image=router_image_path)  
        hop_labels.append(hop_ip)

        
        if idx == 0:
            net.add_edge(router_label or "Local", hop_ip)
        else:
            net.add_edge(hop_labels[idx - 1], hop_ip)

   
    target_label = f"{target} ({domain})" if domain else target
    net.add_node("Target", label=target_label, shape="image", image=target_image_path)
    if hop_labels:
        net.add_edge(hop_labels[-1], "Target")


    output_file = os.path.join(TRACEROUTE_FOLDER, f"traceroute_{domain}.html")
    net.save_graph(output_file)

    print(f"Rappresentazione del traceroute salvata in: {output_file}")


