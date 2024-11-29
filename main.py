from model.core import NetworkCore
from controller.network_controller import NetworkController
from model.strategies.arp_scan_strategy import ArpScanStrategy
from model.strategies.ip_resolver_strategy import IpResolverStrategy
from model.strategies.tracert_strategy import TracertStrategy
from utils.route_analyzer import plot_network_and_route_with_pyvis
from model.subnet_finder import get_local_ip

if __name__ == "__main__":
    # Creazione del Model
    model = NetworkCore()

    # Registrazione delle strategie
    model.register_strategy("arp_scan", ArpScanStrategy())
    model.register_strategy("ip_resolver", IpResolverStrategy())
    model.register_strategy("tracert", TracertStrategy())

    # Creazione del Controller
    controller = NetworkController(model)

    # ARP Scan
    net_info = controller.get_network_info()
    print("Searching for Active Hosts in LAN...")

    subnet_hosts = []
    for interface, net_ip in net_info.items():
        active_hosts = controller.scan_network(net_ip)
        subnet_hosts.extend(active_hosts)

    print("Active Hosts found:")
    for host in subnet_hosts:
        print(host)

    # Risoluzione dell'IP (con dominio opzionale)
    target_ip, domain = controller.resolve_ip(return_domain=True)

    # Traceroute
    trace = controller.trace_route(target_ip)
    local_ip = get_local_ip()
    print("Traceroute Results:")
    for snd, rcv in trace:
        print(rcv)

    # Visualizzazione
    plot_network_and_route_with_pyvis(trace, target_ip, subnet_hosts, local_ip, domain)
