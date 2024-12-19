import tkinter as tk
from tkinter import ttk, messagebox
import os
import threading
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PIL import Image, ImageTk
from model.core import NetworkCore
from controller.network_controller import NetworkController
from model.strategies.arp_scan_strategy import ArpScanStrategy
from model.strategies.ip_resolver_strategy import IpResolverStrategy
from model.strategies.tracert_strategy import TracertStrategy
from utils.route_analyzer import save_local_network, save_traceroute_result
from model.subnet_finder import get_local_ip, get_router_ips, get_network_info

RESULTS_FOLDER = "risultati_scansioni"
LOCAL_SCAN_FOLDER = os.path.join(RESULTS_FOLDER, "scansione_rete_locale")
TRACEROUTE_FOLDER = os.path.join(RESULTS_FOLDER, "traceroute")

class NetworkApp:
    """
    Classe principale che gestisce l'interfaccia grafica e le operazioni.
    """
    
    def __init__(self, root):
        """
        Inizializza la grafica dell'applicazione e crea un modello per l'utilizzo delle strategie.

        Parametri:
        root (tk.Tk): La finestra principale dell'applicazione.
        """
        self.root = root # Finestra principale dell'applicazione
        self.root.title("TopoMap") # Titolo dell'applicazione
        self.root.geometry("800x600") # Dimensione iniziale della finestra
        self.root.state("zoomed")  # Schermo intero con possibilità di ridimensionare
        self.history = []  # Vengono memorizzate le schermate, ovvero i pannelli, per poter tornare indietro
        self.stop_operation = False  # Flag per interrompere le operazioni in corso. Se durante il processo di scansione, l'utente preme il pulsante "Indietro", l'operazione viene interrotta

        # NetworkCore utilizza Facade per gestire le strategie (design pattern strategy) ovvero le funzionalità implementate a parte nel sistema
        # Facade consente quindi di inserire in NetworkCore, le strategie che abbiamo implementato in ArpScan...
        # In questo modo, potremmo avere tanti Network_core differenziati dalle strategie registrate tramite facade
        # Vengono registarte le strategie nell'oggetto model, istanza di NetworkCore
        # Viene creato un controller tramite networkController che ha le stesse strategie - funzionalità del model
        # Il controller è l'oggetto su cui possiamo svolgere le nostre operazioni
        self.model = NetworkCore() 
        self.model.register_strategy("arp_scan", ArpScanStrategy()) 
        self.model.register_strategy("ip_resolver", IpResolverStrategy())
        self.model.register_strategy("tracert", TracertStrategy())
        self.controller = NetworkController(self.model)

        # Definizione dello stile per i componenti usati nell'interfaccia grafica
        self.panel_style = {"bg": "#1E1E1E", "padx": 20, "pady": 20}
        self.button_style = {"font": ("Helvetica", 14), "bg": "#004D73", "fg": "white", "activebackground": "#00334E"}
        self.label_style = {"font": ("Helvetica", 14), "fg": "white", "bg": "#1E1E1E"}

        # Inizializzazione dell'interfaccia grafica, mostrando la schermata di introduzione
        self.setup_intro()

    # ------------ Utility Grafica ------------
    def create_frame(self, **kwargs):
        """
        Crea un nuovo frame con lo stile predefinito.

        Output:
        tk.Frame: Il nuovo frame creato.
        """
        style = {**self.panel_style, **kwargs} 
        return tk.Frame(self.root, **style)

    def create_button(self, parent, text, command, **kwargs):
        """
        Crea un nuovo pulsante con lo stile predefinito.

        Parametri:
        parent (tk.Widget): Il widget genitore del pulsante.
        text (str): Il testo del pulsante.
        command (callable): La funzione da chiamare quando il pulsante viene premuto.

        Output:
        tk.Button: Il nuovo pulsante creato.
        """
        style = {**self.button_style, **kwargs}
        return tk.Button(parent, text=text, command=command, **style)

    def create_label(self, parent, text, **kwargs):
        """
        Crea una nuova etichetta con lo stile predefinito.

        Parametri:
        parent (tk.Widget): Il widget genitore dell'etichetta.
        text (str): Il testo dell'etichetta.
        font (tuple): Il font dell'etichetta.

        Output:
        tk.Label: La nuova etichetta creata.
        """
        style = {**self.label_style, **kwargs}
        return tk.Label(parent, text=text, **style)

    def stop_current_operation(self, frame):
        """
        Ferma l'operazione corrente e ripristina il frame.

        Parametri:
        frame (tk.Frame): Il frame da ripristinare.
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
            self.history.pop()
            if self.history:
                self.history[-1]()
            else:
                self.setup_intro()

    def clear_frame(self):
        """
        Pulisce il contenuto del frame corrente.
        """
        for widget in self.root.winfo_children():
            widget.destroy()

    # ------------ Setup della GUI ------------
    def setup_intro(self):
        """
        Mostra l'interfaccia di introduzione con il logo.
        """
        self.clear_frame()

        # Cambia sfondo del frame
        intro_frame = tk.Frame(self.root, bg="#222222", padx=20, pady=20)
        intro_frame.pack(fill="both", expand=True)

        # Logo dell'applicazione
        logo_path = os.path.join("img", "topomap.png") 
        try:
            logo_image = Image.open(logo_path).resize((200, 200))  
            logo_photo = ImageTk.PhotoImage(logo_image)
            logo_label = tk.Label(intro_frame, image=logo_photo, bg="#222222")
            logo_label.pack(pady=20) 
            self.logo_photo = logo_photo 

        except FileNotFoundError:
            tk.Label(intro_frame, text="Logo non trovato", font=("Helvetica", 12, "italic"), fg="white", bg="#222222").pack(pady=20)

        # Titolo
        tk.Label(
            intro_frame,
            text="Benvenuto/a in TopoMap!",
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
            activebackground="#FFFFFF", 
        ).pack(pady=20)


    def setup_menu(self):
        """
        Mostra il menu principale.
        """
        self.clear_frame()
        frame = self.create_frame()
        frame.pack(fill="both", expand=True)

        self.create_label(frame, "Menu Principale", font=("Helvetica", 20, "bold")).pack(pady=20)

        menu_buttons = [
            ("Scansione della rete locale", self.scan_local_network),
            ("Traceroute verso un dominio/IP", self.perform_traceroute),
            ("Visualizza le scansioni salvate", self.view_saved_scans),
            ("Guida utente", self.show_help),
            ("Esci", self.root.quit),
        ]
        
        for text, command in menu_buttons:
            if text == "Guida utente":
                button = self.create_button(frame, text, command, bg="#00FF00", fg="black")
                button.pack(pady=(70, 5)) 
            else:
                button = self.create_button(frame, text, command)
                button.pack(pady=12)

    # ------------ Metodi per operazioni ------------
    def show_help(self):
        """
        Mostra la guida utente in un pannello più piccolo.
        """
        help_window = tk.Toplevel(self.root)
        help_window.title("Guida Utente")
        help_window.geometry("800x700")

        help_window.update_idletasks()
        width = help_window.winfo_width()
        height = help_window.winfo_height()
        x = (help_window.winfo_screenwidth() // 2) - (width // 2)
        y = (help_window.winfo_screenheight() // 2) - (height // 2)
        help_window.geometry(f'{width}x{height}+{x}+{y}')

        help_text = """
        Benvenuto/a in TopoMap!

        Come utilizzare l'applicazione:

        - Naviga nel menu principale per accedere alle diverse funzionalità.
        - Segui le istruzioni sullo schermo per completare le operazioni desiderate.
        - Utilizza il pulsante "Guida Utente" per visualizzare questa guida in qualsiasi momento.

        Funzionalità del Software:

        1. Scansione della rete locale:
        - Scansiona la rete locale per trovare gli host attivi e i router.
        - Per avviare una scansione, clicca sul pulsante "Scansioni della rete locale" nel menu principale.

        2. Traceroute:
        - Esegue un traceroute dal proprio IP a un dominio/IP specificato.
        - Per avviare un traceroute, clicca sul pulsante "Traceroute" nel menu principale e inserisci il dominio/IP.

        3. Visualizzazione delle scansioni salvate:
        - Mostra una finestra per visualizzare le scansioni salvate.
        - Per visualizzare le scansioni salvate, clicca sul pulsante "Visualizza scansioni salvate" nel menu principale.

        4. Interruzione dell'operazione corrente:
        - Interrompe l'operazione in corso e torna alla schermata precedente.
        - Per interrompere un'operazione, clicca sul pulsante "Indietro".
        
        Altre funzionalità saranno aggiunte in futuro!

        Grazie per aver utilizzato la nostra applicazione!
        """

        help_label = tk.Label(help_window, text=help_text, justify="left", font=("Helvetica", 12))
        help_label.pack(pady=20, padx=20)
        
        close_button = tk.Button(help_window, text="Chiudi", command=help_window.destroy, bg= "#004D73", fg= "white", width=20, height=1)
        close_button.pack(pady=10)
    
    def stop_current_operation(self, frame):
        """
        Interrompe l'operazione in corso e torna alla schermata precedente.
        """
        self.stop_operation = True  # Segna l'operazione come interrotta
        frame.destroy()

        self.setup_menu()  # menu principale
        
    def scan_local_network(self):
        """
        Esegue la scansione della rete locale con un'interfaccia di caricamento.
        """
        self.clear_frame()
        self.stop_operation = False  # Resetta il flag

        frame = self.create_frame()
        frame.pack(fill="both", expand=True)

        self.create_label(frame, "Scansione della rete locale in corso...").pack(pady=10)

        progress = ttk.Progressbar(frame, orient="horizontal", length=300, mode="indeterminate")
        progress.pack(pady=10)
        progress.start()

        self.create_button(frame, "Indietro", command=lambda: self.stop_current_operation(frame)).pack(pady=20)

        def perform_scan():
            try:
                net_info = self.controller.get_network_info()
                subnet_hosts = []
                routers = []

                for interface, net_ip in net_info.items():
                    if self.stop_operation:
                        return  # Interrompe l'operazione
                    subnet_hosts.extend(self.controller.scan_network(net_ip))

                routers = get_router_ips()
                local_ip = get_local_ip()

                if self.stop_operation:
                    return  # Se è stato interrotto, non salvare

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

        frame = self.create_frame()
        frame.pack(fill="both", expand=True)

        self.create_label(frame, "Inserisci dominio o IP:", font=("Helvetica", 18)).pack(pady=10)

        target_entry = tk.Entry(frame, font=("Helvetica", 16), width=30)
        target_entry.pack(pady=10)

        # Barra di avanzamento
        progress = ttk.Progressbar(frame, orient="horizontal", length=300, mode="indeterminate")
        progress.pack(pady=10)

        
        results_frame = self.create_frame(bg="#1E1E1E")
        results_frame.pack(fill="both", expand=True)

        def execute_traceroute():
            """
            Esegue un traceroute verso l'IP di destinazione.

            Parametri:
            target_ip (str): L'indirizzo IP di destinazione.
            """
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

                # Step 3: Scansione della rete locale
                net_info = self.controller.get_network_info()
                subnet_hosts = []
                for interface, net_ip in net_info.items():
                    if self.stop_operation:
                        progress.stop()
                        return
                    subnet_hosts.extend(self.controller.scan_network(net_ip))

                # Step 4: traceroute
                trace = []
                for hop in self.controller.trace_route(target_ip):
                    if self.stop_operation:
                        progress.stop()
                        return
                    trace.append(hop)

                    self.create_label(results_frame, f"Hop: {hop}", fg="orange").pack(pady=2)

                # Step 5: Salva i risultati
                if not self.stop_operation:
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
        self.create_button(frame, "Esegui", command=lambda: threading.Thread(target=execute_traceroute, daemon=True).start()).pack(pady=10)

        # Pulsante per tornare indietro
        self.create_button(frame, "Indietro", command=lambda: self.stop_current_operation(frame)).pack(pady=10)


    def view_saved_scans(self):
        """
        Mostra una finestra per visualizzare le scansioni salvate.
        """
        self.clear_frame()
        frame = self.create_frame()
        frame.pack(fill="both", expand=True)

        self.create_label(frame, "Seleziona il tipo di scansione:", font=("Helvetica", 18)).pack(pady=20)

        # Pulsanti per visualizzare le scansioni
        self.create_button(
            frame,
            "Scansioni della rete locale",
            command=lambda: self.display_scans(LOCAL_SCAN_FOLDER)
        ).pack(pady=10)

        self.create_button(
            frame,
            "Traceroute",
            command=lambda: self.display_scans(TRACEROUTE_FOLDER)
        ).pack(pady=10)

        self.create_button(frame, "Indietro", command=self.setup_menu).pack(side="bottom", pady=20)


    def display_scans(self, folder):
        """
        Mostra le scansioni salvate in una cartella specifica.

        Parametri:
        folder (str): Il percorso della cartella contenente le scansioni salvate.
        """
        self.clear_frame()
        frame = self.create_frame()
        frame.pack(fill="both", expand=True)

    
        self.create_label(frame, f"Scansioni salvate in {os.path.basename(folder)}", font=("Helvetica", 18)).grid(row=0, column=0, columnspan=2, pady=10)

        
        canvas = tk.Canvas(frame, bg="#1E1E1E", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1E1E1E")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
        canvas.configure(yscrollcommand=scrollbar.set)

        
        canvas.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")

        
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        
        if not os.path.exists(folder):
            self.create_label(scrollable_frame, "Cartella non trovata.").pack(pady=10)
        else:
            try:
                scans = [f for f in os.listdir(folder) if f.endswith(".html")]
                if not scans:
                    self.create_label(scrollable_frame, "Nessuna scansione trovata.").pack(pady=10)
                else:
                    for scan in scans:
                        self.create_button(
                            scrollable_frame,
                            scan,
                            command=lambda s=scan: self.open_scan(folder, s),
                            width=50
                        ).pack(pady=5, anchor="center")
            except Exception as e:
                self.create_label(scrollable_frame, f"Errore nell'accesso ai file: {e}").pack(pady=10)

        
        back_button_frame = tk.Frame(frame, bg="#1E1E1E")
        back_button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        self.create_button(back_button_frame, "Indietro", command=self.view_saved_scans).pack()

    def open_scan(self, folder, filename):
        
        filepath = os.path.join(folder, filename)
        try:
            os.startfile(filepath) 
        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile aprire il file: {e}")

    def clear_frame(self):
        """
        Pulisce il contenuto del frame corrente.
        """
        for widget in self.root.winfo_children():
            widget.destroy()
            
# ------------------- ESECUZIONE ----------------------------- #
if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkApp(root)
    root.mainloop()