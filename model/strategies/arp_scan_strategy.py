import nmap
from model.strategies.base_strategy import NetworkOperation

class ArpScanStrategy(NetworkOperation):
    def execute(self, network_range):
        """
        Esegue una scansione ARP e restituisce gli host attivi.
        """
        scanner = nmap.PortScanner()
        scanner.scan(hosts=network_range, arguments='-sn')
        return [host for host in scanner.all_hosts() if scanner[host].state() == "up"]
