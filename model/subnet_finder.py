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
    """
    Raccoglie le informazioni sulle reti disponibili.
    """
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
                # Compute network address in CIDR format
                ip_interface = ipaddress.IPv4Interface(f"{ip_addr}/{netmask}")
                network = ip_interface.network
                network_info[interface] = str(network)  # Network in CIDR format

        except KeyError:
            # If the interface doesn't have an IP, skip it
            pass

    return network_info

def get_router_ips():
    """
    Identifica gli IP dei router o dei gateway predefiniti.
    """
    gateways = ni.gateways()
    router_ips = []

    if ni.AF_INET in gateways:
        for gateway, interface, is_default in gateways[ni.AF_INET]:
            if is_default:  # Considera solo i gateway predefiniti
                router_ips.append((gateway, interface))

    return router_ips

def check_internet_connection():
        """
        Verifica se il dispositivo è connesso a Internet.
        """
        import socket
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False


#---- TEST ----
#print(get_network_info())
