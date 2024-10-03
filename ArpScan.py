from scapy import ARP, Ether, srp


def arp_scan(ip_range):
    # Creare un pacchetto ARP per l'intervallo IP
    arp_request = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp_request

    # Inviare il pacchetto e ricevere le risposte
    result = srp(packet, timeout=2, verbose=0)[0]

    # Elaborare le risposte
    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    return devices

