import PortScan, Tracert, ArpScan, RouteAnalyzer



target_ip = input("Enter target IP: ")
start_port = int(input("Enter start port: "))
end_port = int(input("Enter end port: "))


#for port in range(start_port, end_port + 1):
    #PortScan.scan_port(target_ip, port)




# Scansione di un intervallo di IP
devices = ArpScan.arp_scan("10.10.10.1/24")
print(devices)
