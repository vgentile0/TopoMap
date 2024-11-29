class NetworkFacade:
    def __init__(self):
        self.strategies = {}

    def register_strategy(self, operation_name, strategy):
        self.strategies[operation_name] = strategy

    def execute(self, operation_name, *args, **kwargs):
        if operation_name not in self.strategies:
            raise ValueError(f"Operation {operation_name} not registered.")
        return self.strategies[operation_name].execute(*args, **kwargs)
