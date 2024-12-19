from model.subnet_finder import get_network_info

class NetworkController:
    def __init__(self, model):
        self.model = model

    def attach_view(self, view):
        self.model.attach(view)

    def get_network_info(self):
        """
        Ottiene le informazioni sulla rete locale.
        """
        return get_network_info()

    def scan_network(self, network_range):
        """
        Esegue una scansione ARP sulla rete specificata.
        """
        return self.model.execute_operation("arp_scan", network_range)
    
    def resolve_ip(self, return_domain=False):
        """
        Permette all'utente di scegliere un target IP o dominio.
        Se `return_domain` è True, restituisce sia l'IP che il dominio.
        """
        while True:
            try:
                
                print("Type 1 to scan by domain or 2 to scan by IPv4:")
                ip_type = int(input())
                if ip_type not in [1, 2]:
                    raise ValueError("Invalid option. Please enter 1 for domain or 2 for IP.")

                input_value = input("Enter target domain or IP: ")

                if ip_type == 1 and return_domain:
                    # Risoluzione di dominio e restituzione di IP e dominio
                    domain = input_value
                    target_ip = self.model.execute_operation("ip_resolver", ip_type, input_value)
                    return target_ip, domain
                else:
                    # Solo IP (sia da dominio che da IPv4 diretto)
                    target_ip = self.model.execute_operation("ip_resolver", ip_type, input_value)
                    return (target_ip, None) if return_domain else target_ip

            except ValueError as e:
                print(f"Error: {e}. Please try again.")
            except Exception as e:
                print(f"Unexpected error: {e}. Please try again.")


    def scan_ports(self, target_ip, start_port, end_port):
        """
        Esegue una scansione delle porte su un IP target.
        """
        return self.model.execute_operation("port_scan", target_ip, start_port, end_port)

    def trace_route(self, target):
        """
        Traccia il percorso verso il target specificato.
        """
        return self.model.execute_operation("tracert", target)
    
    def is_valid_ip(self, address):
        import re
        """
        Verifica se una stringa è un indirizzo IP valido.

        Parametri:
        address (str): La stringa da verificare.

        Ritorna:
        bool: True se la stringa è un indirizzo IP valido, False altrimenti.
        """
        try:
            # Verifica se l'indirizzo è un indirizzo IPv4 valido
            pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$") # Definisce il pattern per un indirizzo IPv4 tramite espressione regolare
            return pattern.match(address) is not None
        except:
            return False
        
    def resolve_ip_gui(self, target):
        """
        Risolve un dominio/IP specificato nella GUI.

        Parametri:
        target (str): Il dominio o l'indirizzo IP da risolvere.

        Ritorna:
        tuple: Una tupla contenente l'indirizzo IP risolto e il dominio (se applicabile).
        """
        try:
            if self.is_valid_ip(target):  # Verifica se il target è un indirizzo IP valido
                ip_type = 2
                target_ip = target
                domain = None
            else:
                ip_type = 1
                domain = target
                target_ip = self.model.execute_operation("ip_resolver", ip_type, target)

            if not target_ip:
                # Mostra un messaggio di errore nella GUI se l'IP non porta a nessuna risposta
                raise ValueError("Errore", "L'indirizzo IP o il dominio non ha portato a nessuna risposta.")
                return None, None

            return target_ip, domain
        except Exception as e:
            # Mostra un messaggio di errore nella GUI
            raise ValueError(f"Errore nella risoluzione: {e}")