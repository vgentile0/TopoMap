import netifaces as ni
import ipaddress

def get_network_info():
    interfaces = ni.interfaces()
    network_info = {}

    for interface in interfaces:
        try:
            # Ottieni indirizzo IPv4 e netmask della rete
            ip_info = ni.ifaddresses(interface)[ni.AF_INET][0]
            ip_addr = ip_info['addr']
            netmask = ip_info['netmask']

            # Controlla se l'indirizzo non è di loopback (127.x.x.x)
            if not ip_addr.startswith("127."):
                # Calcola la rete in formato CIDR
                ip_interface = ipaddress.IPv4Interface(f"{ip_addr}/{netmask}")
                network = ip_interface.network
                network_info[interface] = str(network)  # Rete in formato CIDR (es. 192.168.1.0/24)

        except KeyError:
            # Se l'interfaccia non ha un indirizzo IPv4, saltala
            pass

    return network_info

print(get_network_info())
