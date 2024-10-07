import socket


class PortScanner:
    def __init__(self, ip, timeout=1):
        self.ip = ip
        self.timeout = timeout
        self.portDic = {}

    def scan_port(self, port):
        """Scansiona una singola porta e aggiorna il dizionario con lo stato."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(self.timeout)  # Imposta il timeout
        result = sock.connect_ex((self.ip, port))  # Tenta la connessione alla porta

        # Verifica se la porta è aperta o chiusa
        if result == 0:
           # print(f"Port {port} is open")
            self.portDic[port] = True
        else:
            #print(f"Port {port} is closed")
            self.portDic[port] = False

        sock.close()

    def scan_ports(self, start_port, end_port):
        """Scansiona un intervallo di porte specificato."""
        for port in range(start_port, end_port + 1):
            self.scan_port(port)

        return self.portDic


