class Subject:
    """
    Classe osservabile che notifica gli osservatori quando lo stato cambia.
    """
    def __init__(self):
        self._observers = []  # Lista degli osservatori registrati

    def attach(self, observer):
        """
        Aggiunge un osservatore alla lista.
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        """
        Rimuove un osservatore dalla lista.
        """
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, *args, **kwargs):
        """
        Notifica tutti gli osservatori degli aggiornamenti.
        """
        for observer in self._observers:
            observer.update(*args, **kwargs)


class Observer:
    """
    Interfaccia per gli osservatori.
    """
    def update(self, *args, **kwargs):
        """
        Metodo chiamato dall'oggetto osservabile per notificare aggiornamenti.
        """
        raise NotImplementedError("La classe concreta deve implementare il metodo 'update'.")
