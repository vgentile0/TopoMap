from utils.route_analyzer import save_local_network, save_traceroute_result, create_results_directories
from model.subnet_finder import get_router_ips, get_local_ip, check_internet_connection

def menu():
    create_results_directories()
    """
    Creazione del menu principale.
    """
    banner = """
    +--------------------------+
    |          TOPOMAP         |   
    +--------------------------+                                                                          
    """
    print(banner)
    print("1. Scansione della rete locale")
    print("2. Traceroute fino a un dominio/IP specificato")
    print("3. Guida all'uso")
    print("4. Esci")
    choice = input("Scegli un'opzione (1-4): ")
    return choice
    
def scan_local_network(controller):

    if not check_internet_connection():
        print("Errore: Nessuna connessione a Internet rilevata. Assicurati di essere connesso alla rete e riprova.")
        return None, None

    print("\nScansione della rete locale in corso...")
    net_info = controller.get_network_info()
    subnet_hosts = []

    # Scansione della rete per gli host attivi
    for interface, net_ip in net_info.items():
        print(f"Scanning network range: {net_ip}")
        active_hosts = controller.scan_network(net_ip)
        subnet_hosts.extend(active_hosts)

    #IP dei router
    router_ips = get_router_ips()
    print("\nRouter trovati:")
    for router_ip, interface in router_ips:
        print(f"Router IP: {router_ip} (Interfaccia: {interface})")

    print("\nHost attivi trovati:")
    for host in subnet_hosts:
        print(host)

    # l'IP locale del dispositivo
    local_ip = get_local_ip()
    print(f"\nIl tuo IP locale è: {local_ip}")

    save_local_network(subnet_hosts, local_ip, router_ip)

    return subnet_hosts, router_ips


def perform_traceroute(controller, subnet_hosts):
    """
    Esegue un traceroute dal proprio IP a un dominio/IP specificato.
    """
    local_ip = get_local_ip()
    try:
        target_ip, domain = controller.resolve_ip(return_domain=True)
        trace = controller.trace_route(target_ip)
        save_traceroute_result(trace, target_ip, subnet_hosts, local_ip, domain)
    except ValueError as e:
        print(f"Errore: {e}")
        
def show_guide(controller):
    """
    Mostra una guida all'utente.
    """
    print("\n--- Guida all'uso ---")
    print("1. Scansione della rete locale:")
    print("   - Scansiona la rete locale per trovare gli host attivi e i router.")
    print("2. Traceroute fino a un dominio/IP specificato:")
    print("   - Esegue un traceroute dal proprio IP a un dominio/IP specificato.")
    print("3. Esci:")
    print("   - Termina il programma.")
