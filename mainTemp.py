import  subnetFinder, ArpScan, PortScan, Tracert, RouteAnalyzer
from PortScan import PortScanner

if __name__ == "__main__":
    # ARP Scan
    net_info= subnetFinder.get_network_info()
    print("Searching for Active Host in LAN")

    #scansione device su subnet
    for interface, net_ip in net_info.items():
        subnetHost= ArpScan.scan_hosts(net_ip)

    print("Host attivi trovati:")
    for host in subnetHost :
        print(host)

    target_ip = input("Enter target IP: ")
    start_port = int(input("Enter start port: "))
    end_port = int(input("Enter end port: "))
    """""""""
    # Port Scan
    scanner = PortScan.PortScanner(target_ip)
    result = scanner.scan_ports(start_port, end_port)  # Scansiona le porte dal 20 al 25
    print(result)
"""""""""
    #Trace Route
    trace= Tracert.trace_route(target_ip)
    print(trace)

    RouteAnalyzer.plot_route(trace, target_ip)
