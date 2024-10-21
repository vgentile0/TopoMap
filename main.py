import subnetFinder, ArpScan, PortScan, Tracert, RouteAnalyzer, IpResolver

if __name__ == "__main__":
    # ARP Scan
    net_info = subnetFinder.get_network_info()
    print("Searching for Active Hosts in LAN")

    subnet_hosts = []  # List initialization for active lan hosts
    for interface, net_ip in net_info.items():
        active_hosts = ArpScan.scan_hosts(net_ip)
        subnet_hosts.extend(active_hosts)  # Add active lan host to list

    print("Active Host found:")
    for host in subnet_hosts:
        print(host)

    target_ip = IpResolver.ipHandler()
    start_port = int(input("Enter start port: "))
    end_port = int(input("Enter end port: "))

    # Port Scan
    scanner = PortScan.PortScanner(target_ip)
    result = scanner.scan_ports(start_port, end_port)
    print(result)

    # Trace Route
    trace = Tracert.trace_route(target_ip)
    print(trace)

    # Graph
    RouteAnalyzer.plot_route(trace, target_ip, subnet_hosts)
