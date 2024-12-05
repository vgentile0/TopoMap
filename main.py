from model.core import NetworkCore
from controller.network_controller import NetworkController
from model.strategies.arp_scan_strategy import ArpScanStrategy
from model.strategies.ip_resolver_strategy import IpResolverStrategy
from model.strategies.tracert_strategy import TracertStrategy
from utils.route_analyzer import save_local_network, save_traceroute_result, create_results_directories
from model.subnet_finder import get_network_info, get_router_ips, get_local_ip



def menu():
    create_results_directories()
    """
    Mostra il menu principale e restituisce la scelta dell'utente.
    """
    print("\n--- Network Topology Mapper ---")
    print("1. Scansione della rete locale")
    print("2. Traceroute fino a un dominio/IP specificato")
    print("3. Esci")
    choice = input("Scegli un'opzione (1-3): ")
    return choice

def scan_local_network(controller):
    """
    Scansiona la rete locale, mostra gli IP attivi e identifica gli IP dei router.
    """
    print("\nScansione della rete locale in corso...")
    net_info = controller.get_network_info()
    subnet_hosts = []

    # Scansione della rete per gli host attivi
    for interface, net_ip in net_info.items():
        print(f"Scanning network range: {net_ip}")
        active_hosts = controller.scan_network(net_ip)
        subnet_hosts.extend(active_hosts)

    # Ottieni gli IP dei router
    router_ips = get_router_ips()
    print("\nRouter trovati:")
    #RIMUOVERE INTERFACCIA A ROUTER SENNO NON SI VEDE NIENTE
    for router_ip, interface in router_ips:
        print(f"Router IP: {router_ip} (Interfaccia: {interface})")

    print("\nHost attivi trovati:")
    for host in subnet_hosts:
        print(host)

    # Ottieni l'IP locale del dispositivo
    local_ip = get_local_ip()
    print(f"\nIl tuo IP locale è: {local_ip}")
    #al posto di router_ip si può inserire router_ips per avere anche l'interfaccia del router
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

def main():
    # Configura il modello e il controller
    model = NetworkCore()
    model.register_strategy("arp_scan", ArpScanStrategy())
    model.register_strategy("ip_resolver", IpResolverStrategy())
    model.register_strategy("tracert", TracertStrategy())
    controller = NetworkController(model)

    subnet_hosts = []  # Memorizza gli host trovati nella rete locale

    while True:
        choice = menu()

        if choice == "1":
            # Scansione della rete locale
            subnet_hosts = scan_local_network(controller)
        elif choice == "2":
            # Traceroute fino a un target
            perform_traceroute(controller, subnet_hosts)
        elif choice == "3":
            print("\nAlla prossima scansione! Arrivederci.")
            break
        else:
            print("\nScelta non valida. Riprova.")


if __name__ == "__main__":
    main()
