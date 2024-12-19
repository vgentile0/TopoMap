import tkinter as tk
from tkinter import ttk, messagebox
import os
import threading
from model.core import NetworkCore
from controller.network_controller import NetworkController
from model.strategies.arp_scan_strategy import ArpScanStrategy
from model.strategies.ip_resolver_strategy import IpResolverStrategy
from model.strategies.tracert_strategy import TracertStrategy
from utils.route_analyzer import save_local_network, save_traceroute_result
from model.subnet_finder import get_local_ip, get_router_ips, get_network_info
from PIL import Image, ImageTk  # Modulo per gestire immagini

# Percorsi delle directory
RESULTS_FOLDER = "risultati_scansioni"
LOCAL_SCAN_FOLDER = os.path.join(RESULTS_FOLDER, "scansione_rete_locale")
TRACEROUTE_FOLDER = os.path.join(RESULTS_FOLDER, "traceroute")


class NetworkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Topology Mapper")
        self.root.geometry("800x600")
        self.root.state("zoomed")  # Schermo intero con possibilità di ridimensionare
        self.history = []  # Per navigare tra le schermate
        self.stop_operation = False  # Flag per interrompere operazioni

        # Configura il modello e il controller
        self.model = NetworkCore()
        self.model.register_strategy("arp_scan", ArpScanStrategy())
        self.model.register_strategy("ip_resolver", IpResolverStrategy())
        self.model.register_strategy("tracert", TracertStrategy())
        self.controller = NetworkController(self.model)

        # Setup dell'interfaccia
        self.setup_intro()
        
        # Stile dei botton delle operazioni
        self.button_style = {
            "font": ("Helvetica", 18),
            "width": 30,
            "bg": "#004D73",
            "fg": "white",
            "activebackground": "#00334E",
        }
    
    
        
    def stop_current_operation(self, frame):
        """
        Interrompe l'operazione in corso e torna alla schermata precedente.
        """
        self.stop_operation = True
        frame.destroy()
        self.go_back()

    def navigate_to(self, setup_function):
        """
        Naviga verso una nuova schermata e salva la precedente nella cronologia.
        """
        self.history.append(setup_function)
        setup_function()

    def go_back(self):
        """
        Torna alla schermata precedente.
        """
        if self.history:
            self.history.pop()  # Rimuove la schermata corrente
            if self.history:
                self.history[-1]()  # Carica la schermata precedente
            else:
                self.setup_intro()  # Torna all'introduzione

    def setup_intro(self):
            """
            Mostra l'interfaccia di introduzione con il logo.
            """
            self.clear_frame()

            # Cambia sfondo del frame
            intro_frame = tk.Frame(self.root, bg="#222222", padx=20, pady=20)
            intro_frame.pack(fill="both", expand=True)

            # Logo dell'applicazione
            logo_path = os.path.join("img", "topomap.png")  # Percorso dell'immagine
            try:
                logo_image = Image.open(logo_path).resize((200, 200))  # Ridimensiona l'immagine
                logo_photo = ImageTk.PhotoImage(logo_image)
                tk.Label(intro_frame, image=logo_photo, bg="#222222").pack(pady=20)
                self.logo_photo = logo_photo  
            except FileNotFoundError:
                tk.Label(intro_frame, text="Logo non trovato", font=("Helvetica", 12, "italic"), fg="white", bg="#222222").pack(pady=20)

            # Titolo
            tk.Label(
                intro_frame,
                text="Welcome to Network Topology Mapper!",
                font=("Helvetica", 26, "bold"),
                fg="white",
                bg="#222222",
            ).pack(pady=20)

            # Pulsante Inizia
            tk.Button(
                intro_frame,
                text="Continua",
                command=lambda: self.navigate_to(self.setup_menu),
                font=("Helvetica", 18),
                width=20,
                bg="#0000FF",  # Colore del pulsante
                fg="white",  # Colore del testo
                activebackground="#FFFFFF",  # Colore attivo
            ).pack(pady=20)

    def setup_menu(self):
        """
        Mostra il menu principale.
        """
        self.clear_frame()

        menu_frame = tk.Frame(self.root, bg="#1E1E1E", padx=20, pady=20)  # Sfondo scuro
        menu_frame.pack(fill="both", expand=True)

        tk.Label(menu_frame, text="Menu Principale", font=("Helvetica", 20, "bold"), fg="white", bg="#1E1E1E").pack(pady=50)

        # Stile pulsanti

        tk.Button(
            menu_frame,
            text="Scansione della rete locale",
            command=lambda: self.navigate_to(self.scan_local_network),
            **self.button_style,
        ).pack(pady=10)

        tk.Button(
            menu_frame,
            text="Traceroute verso un dominio/IP",
            command=lambda: self.navigate_to(self.perform_traceroute),
            **self.button_style,
        ).pack(pady=10)

        tk.Button(
            menu_frame,
            text="Visualizza scansioni salvate",
            command=lambda: self.navigate_to(self.view_saved_scans),
            **self.button_style,
        ).pack(pady=10)

        tk.Button(
            menu_frame,
            text="Esci",
            command=self.root.quit,
            **self.button_style,
        ).pack(pady=10)


    def scan_local_network(self):
        """
        Esegue la scansione della rete locale con un'interfaccia di caricamento.
        """
        self.clear_frame()

        self.stop_operation = False  # Resetta il flag

        scan_frame = tk.Frame(self.root, padx=20, pady=20)
        scan_frame.pack(fill="both", expand=True)

        tk.Label(scan_frame, text="Scansione della rete locale in corso...", font=("Helvetica", 14)).pack(pady=10)

        progress = ttk.Progressbar(scan_frame, orient="horizontal", length=300, mode="indeterminate")
        progress.pack(pady=10)
        progress.start()

        tk.Button(
            scan_frame,
            text="Indietro",
            command=lambda: self.stop_current_operation(scan_frame),
            **self.button_style,
        ).pack(pady=20)

        def perform_scan():
            try:
                net_info = self.controller.get_network_info()
                subnet_hosts = []
                routers = []

                for interface, net_ip in net_info.items():
                    if self.stop_operation:
                        return  # Interrompe l'operazione
                    active_hosts = self.controller.scan_network(net_ip)
                    subnet_hosts.extend(active_hosts)

                if self.stop_operation:
                    return  # Interrompe l'operazione

                routers = get_router_ips()
                local_ip = get_local_ip()

                save_local_network(subnet_hosts, local_ip, [r[0] for r in routers])
                if not self.stop_operation:
                    messagebox.showinfo("Successo", "Scansione completata e salvata.")
            except Exception as e:
                if not self.stop_operation:
                    messagebox.showerror("Errore", f"Errore durante la scansione: {e}")
            finally:
                if not self.stop_operation:
                    self.setup_menu()

        threading.Thread(target=perform_scan, daemon=True).start()


    def perform_traceroute(self):
        """
        Esegue un traceroute verso un dominio/IP specificato dall'utente nella GUI.
        """
        self.clear_frame()
        self.stop_operation = False  # Resetta il flag

        traceroute_frame = tk.Frame(self.root, bg="#1E1E1E", padx=20, pady=20)
        traceroute_frame.pack(fill="both", expand=True)

        # Intestazione
        tk.Label(
            traceroute_frame,
            text="Inserisci dominio o IP:",
            font=("Helvetica", 18),
            fg="white",
            bg="#1E1E1E",
        ).pack(pady=10)

        # Input dell'utente
        target_entry = tk.Entry(traceroute_frame, font=("Helvetica", 16), width=30)
        target_entry.pack(pady=5)

        # Barra di avanzamento
        progress = ttk.Progressbar(traceroute_frame, orient="horizontal", length=300, mode="indeterminate")
        progress.pack(pady=10)

        # Risultati del traceroute
        results_frame = tk.Frame(traceroute_frame, bg="#1E1E1E")
        results_frame.pack(fill="both", expand=True)


        def execute_traceroute():
            target = target_entry.get().strip()
            if not target:
                messagebox.showerror("Errore", "Devi inserire un dominio o IP valido.")
                return

            progress.start()
            try:
                # Step 1: Ottieni l'IP locale
                local_ip = get_local_ip()

                # Step 2: Risolvi il dominio/IP target
                target_ip, domain = self.controller.resolve_ip_gui(target)

                # Step 3: Scansione della rete locale per identificare host attivi e router
                net_info = self.controller.get_network_info()
                subnet_hosts = []
                router_ips = []

                for interface, net_ip in net_info.items():
                    if self.stop_operation:
                        progress.stop()
                        return
                    active_hosts = self.controller.scan_network(net_ip)
                    subnet_hosts.extend(active_hosts)

                router_ips = get_router_ips()

                # Aggiorna dinamicamente i risultati della scansione
                tk.Label(
                    results_frame,
                    text=f"Rete Locale: {len(subnet_hosts)} host attivi trovati.",
                    font=("Helvetica", 14),
                    fg="cyan",
                    bg="#1E1E1E",
                ).pack(pady=5)

                # Step 4: Esegue il traceroute
                trace = []
                for hop in self.controller.trace_route(target_ip):
                    if self.stop_operation:
                        progress.stop()
                        return
                    trace.append(hop)

                    # Aggiorna dinamicamente i risultati del traceroute
                    tk.Label(
                        results_frame,
                        text=f"{hop}",
                        font=("Helvetica", 14),
                        fg="orange",
                        bg="#1E1E1E",
                    ).pack(pady=2)

                # Step 5: Salva i risultati
                save_traceroute_result(trace, target_ip, subnet_hosts, local_ip, domain)

                messagebox.showinfo("Successo", "Traceroute completato e salvato.")
            except ValueError as e:
                if not self.stop_operation:
                    messagebox.showerror("Errore", f"Errore: {e}")
            except Exception as e:
                if not self.stop_operation:
                    messagebox.showerror("Errore", f"Errore inaspettato: {e}")
            finally:
                progress.stop()
                if not self.stop_operation:
                    self.setup_menu()

        # Pulsante per avviare il traceroute
        tk.Button(
            traceroute_frame,
            text="Esegui",
            command=lambda: threading.Thread(target=execute_traceroute, daemon=True).start(),
            font=("Helvetica", 14),
            bg="#004D73",
            fg="white",
            activebackground="#00334E",
        ).pack(pady=10)

        # Pulsante per tornare indietro
        tk.Button(
            traceroute_frame,
            text="Indietro",
            command=lambda: self.stop_current_operation(traceroute_frame),
            font=("Helvetica", 14),
            bg="#004D73",
            fg="white",
            activebackground="#00334E",
        ).pack(pady=10)




    def view_saved_scans(self):
        """
        Mostra una finestra per visualizzare le scansioni salvate.
        """
        self.clear_frame()

        scan_type_frame = tk.Frame(self.root, padx=20, pady=20)
        scan_type_frame.pack(fill="both", expand=True)

        tk.Label(scan_type_frame, text="Seleziona il tipo di scansione:", font=("Helvetica", 18, "bold")).pack(pady=30)
        
        tk.Button(
            scan_type_frame,
            text="Scansioni della rete locale",
            command=lambda: self.display_scans(LOCAL_SCAN_FOLDER),
            font=("Helvetica", 16),
            width=30,
        ).pack(pady=10)

        tk.Button(
            scan_type_frame,
            text="Traceroute",
            command=lambda: self.display_scans(TRACEROUTE_FOLDER),
            font=("Helvetica", 16),
            width=30,
        ).pack(pady=10)

        tk.Button(
            scan_type_frame,
            text="Indietro",
            command=self.go_back,
            font=("Helvetica", 16),
            width=20,
        ).pack(pady=20)

    def display_scans(self, folder):
        """
        Mostra i file di scansione salvati in una directory specifica.
        """
        self.clear_frame()

        display_frame = tk.Frame(self.root, padx=20, pady=20)
        display_frame.pack(fill="both", expand=True)

        tk.Label(display_frame, text=f"Scansioni salvate in {os.path.basename(folder)}", font=("Helvetica", 18, "bold")).pack(pady=30)

        # Assicuriamoci che la directory esista
        if not os.path.exists(folder):
            tk.Label(display_frame, text="Cartella non trovata.", font=("Helvetica", 16)).pack(pady=10)
        else:
            try:
                # Elenca i file HTML nella directory
                scans = [f for f in os.listdir(folder) if f.endswith(".html")]
                if not scans:
                    tk.Label(display_frame, text="Nessuna scansione trovata.", font=("Helvetica", 16)).pack(pady=10)
                else:
                    for scan in scans:
                        tk.Button(
                            display_frame,
                            text=scan,
                            command=lambda s=scan: self.open_scan(folder, s),
                            font=("Helvetica", 14),
                            width=50,
                        ).pack(pady=5)
            except Exception as e:
                tk.Label(display_frame, text=f"Errore nell'accesso ai file: {e}", font=("Helvetica", 16)).pack(pady=10)

        # Pulsante Indietro
        tk.Button(
            display_frame,
            text="Indietro",
            command=self.go_back,
            font=("Helvetica", 16),
            width=20,
        ).pack(pady=20)


    def open_scan(self, folder, filename):
        
        filepath = os.path.join(folder, filename)
        try:
            os.startfile(filepath)  # Apre il file con il programma predefinito
        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile aprire il file: {e}")

    def clear_frame(self):
        """
        Pulisce il contenuto del frame corrente.
        """
        for widget in self.root.winfo_children():
            widget.destroy()
            

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkApp(root)
    root.mainloop()