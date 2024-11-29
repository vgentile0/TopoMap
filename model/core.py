from observer import Subject
from model.facade import NetworkFacade

class NetworkCore(Subject):
    def __init__(self):
        super().__init__()
        self.facade = NetworkFacade()

    def register_strategy(self, operation_name, strategy):
        self.facade.register_strategy(operation_name, strategy)

    def execute_operation(self, operation_name, *args, **kwargs):
        results = self.facade.execute(operation_name, *args, **kwargs)
        self.notify(operation=operation_name, results=results)
        return results
