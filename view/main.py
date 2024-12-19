import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.core import NetworkCore
from controller.network_controller import NetworkController
from model.strategies.arp_scan_strategy import ArpScanStrategy
from model.strategies.ip_resolver_strategy import IpResolverStrategy
from model.strategies.tracert_strategy import TracertStrategy
from menu_CLI import *

def main():
    """
    Funzione principale del programma.
    """
    model = NetworkCore()
    model.register_strategy("arp_scan", ArpScanStrategy())
    model.register_strategy("ip_resolver", IpResolverStrategy())
    model.register_strategy("tracert", TracertStrategy())
    controller = NetworkController(model)

    subnet_hosts = []

    while True:
        choice = menu()

        if choice == "1":
            subnet_hosts = scan_local_network(controller)
        elif choice == "2":
            perform_traceroute(controller, subnet_hosts)
        elif choice == "3":
            show_guide(controller)
        elif choice == "4":
            print("\nAlla prossima scansione! Arrivederci.")
            break
        else:
            print("\nScelta non valida. Riprova.")


if __name__ == "__main__":
    main()
