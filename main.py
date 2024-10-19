import subnetFinder, ArpScan, PortScan, Tracert, RouteAnalyzer
from PortScan import PortScanner

if __name__ == "__main__":
    # ARP Scan
    net_info = subnetFinder.get_network_info()
    print("Searching for Active Hosts in LAN")

    subnet_hosts = []  # Lista per raccogliere gli host attivi
    for interface, net_ip in net_info.items():
        active_hosts = ArpScan.scan_hosts(net_ip)
        subnet_hosts.extend(active_hosts)  # Aggiungi gli host attivi alla lista

    print("Host attivi trovati:")
    for host in subnet_hosts:
        print(host)

    target_ip = input("Enter target IP: ")
    start_port = int(input("Enter start port: "))
    end_port = int(input("Enter end port: "))

    # Port Scan
    scanner = PortScan.PortScanner(target_ip)
    result = scanner.scan_ports(start_port, end_port)  # Scansiona le porte
    print(result)

    # Trace Route
    trace = Tracert.trace_route(target_ip)
    print(trace)

    # Visualizza il percorso graficamente, passando anche gli host attivi
    RouteAnalyzer.plot_route(trace, target_ip, subnet_hosts)
