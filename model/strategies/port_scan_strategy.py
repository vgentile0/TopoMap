from model.strategies.base_strategy import NetworkOperation
from model.PortScan import PortScanner

class PortScanStrategy(NetworkOperation):
    def execute(self, target_ip, start_port, end_port):
        """
        Esegue una scansione delle porte su un target IP.
        """
        scanner = PortScanner(target_ip)
        return scanner.scan_ports(start_port, end_port)
