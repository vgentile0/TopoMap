from scapy.layers.inet import traceroute
from model.strategies.base_strategy import NetworkOperation
from model.subnet_finder import get_local_ip

class TracertStrategy(NetworkOperation):
    def execute(self, target):
        """
        Esegue un traceroute dall'IP locale al target specificato.
        Rimuove IP duplicati mantenendo l'ordine degli hop.
        """
        local_ip = get_local_ip()
        print(f"Local IP: {local_ip}")

        # Esegui il traceroute verso il target
        result, _ = traceroute(target)

        # Filtra e mantiene solo hop univoci in ordine
        seen_ips = set()
        filtered_result = []

        # Aggiungi l'IP locale come primo hop
        filtered_result.append(("Local", local_ip))
        seen_ips.add(local_ip)

        for snd, rcv in result:
            if rcv.src not in seen_ips:
                filtered_result.append((snd, rcv.src))
                seen_ips.add(rcv.src)

        return filtered_result
