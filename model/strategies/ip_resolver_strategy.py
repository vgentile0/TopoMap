import socket
from model.strategies.base_strategy import NetworkOperation

class IpResolverStrategy(NetworkOperation):
    def execute(self, ip_type, input_value):
        """
        Risolve un dominio o accetta direttamente un IP.
        """
        if ip_type == 1:  # Risoluzione del dominio
            if not input_value.startswith("www."):
                input_value = "www." + input_value
            try:
                return socket.gethostbyname(input_value)
            except socket.gaierror:
                raise ValueError("Invalid domain name.")
        elif ip_type == 2:  # IP diretto
            return input_value
        else:
            raise ValueError("Invalid IP type.")
