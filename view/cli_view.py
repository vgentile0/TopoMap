from observer import Observer

class CLIView(Observer):
    def __init__(self, controller):
        self.controller = controller
        self.controller.attach_view(self)

    def update(self, *args, **kwargs):
        """
        Metodo chiamato quando il Model notifica aggiornamenti.
        """
        operation = kwargs.get("operation")
        results = kwargs.get("results")
        print(f"\n[RESULT - {operation}]:")
        print(results)

    def start(self):
        print("Welcome to Network Topology Mapper")

        # Scelta dell'IP
        use_manual_ip = input("Type 1 to enter IP manually, or 2 to auto-detect: ")
        if use_manual_ip == "1":
            target_ip = input("Enter target IP: ")
            network_range = input("Enter network range (e.g., 192.168.1.0/24): ")
        elif use_manual_ip == "2":
            try:
                # Ottieni automaticamente il network range
                network_range = self.controller.get_default_ip()
                target_ip = network_range.split('/')[0]  # Prende solo l'IP, senza CIDR
                print(f"Auto-detected target IP: {target_ip}")
                print(f"Auto-detected network range: {network_range}")
            except RuntimeError as e:
                print(f"Error: {e}")
                return
        else:
            print("Invalid choice. Exiting.")
            return

        # Scansione ARP
        print(f"Scanning network range: {network_range}")
        self.controller.scan_network(network_range)

        # Scansione delle porte
        start_port = int(input("Enter start port: "))
        end_port = int(input("Enter end port: "))
        self.controller.scan_ports(target_ip, start_port, end_port)

        # Traceroute
        print("Starting traceroute...")
        self.controller.trace_route(target_ip)
