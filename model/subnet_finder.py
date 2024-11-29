import netifaces as ni
import ipaddress

def get_local_ip():
    """
    Rileva l'indirizzo IP locale del dispositivo su cui è in esecuzione il programma.
    """
    interfaces = ni.interfaces()
    for interface in interfaces:
        try:
            ip_info = ni.ifaddresses(interface)[ni.AF_INET][0]
            ip_addr = ip_info['addr']
            if not ip_addr.startswith("127."):  # Esclude loopback
                return ip_addr
        except KeyError:
            continue
    raise RuntimeError("Impossibile rilevare l'IP locale.")

def get_network_info():
    interfaces = ni.interfaces()
    network_info = {}

    for interface in interfaces:
        try:
            # Retrieve IPv4 & netmask
            ip_info = ni.ifaddresses(interface)[ni.AF_INET][0]
            ip_addr = ip_info['addr']
            netmask = ip_info['netmask']

            # Check if IP is loopback (127.x.x.x)
            if not ip_addr.startswith("127."):
                # Compute newtork addres in CIDR format
                ip_interface = ipaddress.IPv4Interface(f"{ip_addr}/{netmask}")
                network = ip_interface.network
                network_info[interface] = str(network)  # Network in CIDR format (eg. 192.168.1.0/24)

        except KeyError:
            # If the interface doesn't have IP skip
            pass

    return network_info

#---- TEST ----
#print(get_network_info())
