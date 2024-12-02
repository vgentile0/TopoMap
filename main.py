from model.core import NetworkCore
from controller.network_controller import NetworkController
from model.strategies.arp_scan_strategy import ArpScanStrategy
from model.strategies.ip_resolver_strategy import IpResolverStrategy
from model.strategies.tracert_strategy import TracertStrategy
from utils.route_analyzer import plot_network_and_route_with_pyvis
from model.subnet_finder import get_local_ip


def menu():
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
    Scansiona la rete locale e mostra gli IP attivi.
    """
    print("\nScansione della rete locale in corso...")
    net_info = controller.get_network_info()
    subnet_hosts = []
    for interface, net_ip in net_info.items():
        print(f"Scanning network range: {net_ip}")
        active_hosts = controller.scan_network(net_ip)
        subnet_hosts.extend(active_hosts)
    print("\nHost attivi trovati:")
    for host in subnet_hosts:
        print(host)
    return subnet_hosts


def perform_traceroute(controller, subnet_hosts):
    """
    Esegue un traceroute dal proprio IP a un dominio/IP specificato dall'utente.
    """
    # Ottieni l'IP locale
    local_ip = get_local_ip()
    print(f"\nIl tuo IP locale è: {local_ip}")

    # Risoluzione del dominio o IP target
    try:
        target_ip, domain = controller.resolve_ip(return_domain=True)
        print(f"Traceroute verso {target_ip} ({domain or 'No domain'}) in corso...")
    except ValueError as e:
        print(f"Errore: {e}")
        return

    # Esegui il traceroute
    trace = controller.trace_route(target_ip)
    print("\nRisultati del Traceroute:")
    for snd, rcv in trace:
        print(rcv)

    # Visualizza il percorso
    plot_network_and_route_with_pyvis(trace, target_ip, subnet_hosts, local_ip, domain)


def main():
    # Configura il modello e il controller
    model = NetworkCore()
    model.register_strategy("arp_scan", ArpScanStrategy())
    model.register_strategy("ip_resolver", IpResolverStrategy())
    model.register_strategy("tracert", TracertStrategy())
    controller = NetworkController(model)

    subnet_hosts = []  # Memorizza gli host trovati nella rete locale

    # Ciclo principale
    while True:
        choice = menu()

        if choice == "1":
            # Scansione della rete locale
            subnet_hosts = scan_local_network(controller)
        elif choice == "2":
            # Traceroute fino a un target
            if not subnet_hosts:
                print("\nDevi prima scansionare la rete locale (opzione 1) per ottenere il tuo IP.")
            else:
                perform_traceroute(controller, subnet_hosts)
        elif choice == "3":
            print("\nGrazie per aver usato Network Topology Mapper. Arrivederci!")
            break
        else:
            print("\nScelta non valida. Riprova.")


if __name__ == "__main__":
    main()
