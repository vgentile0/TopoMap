import nmap


def scan_hosts(network_range):

    # Create instance of nmap.PortScanner
    nm = nmap.PortScanner()

    # Scan with parameter '-sn' for ping scan
    nm.scan(hosts=network_range, arguments='-sn')

    # Initialize active host list
    active_hosts = []

    # Iteriamo tra i risultati della scansione
    for host in nm.all_hosts():
        if nm[host].state() == "up":
            active_hosts.append(host)
        # TO BE ADDED: controllo ed eliminazione duplicati

    return active_hosts


