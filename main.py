import  subnetFinder, ArpScan, PortScan

if __name__ == "__main__":
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


