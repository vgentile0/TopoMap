import nmap


def scan_hosts(network_range):
    # Creiamo un'istanza dell'oggetto nmap.PortScanner
    nm = nmap.PortScanner()

    # Eseguiamo la scansione usando il parametro '-sn' per il ping scan
    nm.scan(hosts=network_range, arguments='-sn')

    # Lista degli host attivi
    active_hosts = []

    # Iteriamo tra i risultati della scansione
    for host in nm.all_hosts():
        if nm[host].state() == "up":
            active_hosts.append(host)

    return active_hosts


# Esempio di utilizzo
if __name__ == "__main__":
    network_range = '10.10.10.1/24'  # Specifica la tua subnet
    active_hosts = scan_hosts(network_range)

    print("Host attivi trovati:")
    for host in active_hosts:
        print(host)
