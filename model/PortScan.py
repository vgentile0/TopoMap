import socket


class PortScanner:
    def __init__(self, ip, timeout=1):
        self.ip = ip
        self.timeout = timeout
        self.portDic = {}

    def scan_port(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(self.timeout)  # Set timeout
        result = sock.connect_ex((self.ip, port))  # Try connection to port

        # Check if port is open
        if result == 0:
           # --- TEST ---
           # print(f"Port {port} is open")
            self.portDic[port] = True
        else:
            # --- TEST ---
            #print(f"Port {port} is closed")
            self.portDic[port] = False

        sock.close()

    def scan_ports(self, start_port, end_port):
        # Scan defined port range
        for port in range(start_port, end_port + 1):
            self.scan_port(port)

        return self.portDic


