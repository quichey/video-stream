from api.util.db_engine import DataBaseEngine


class StateModule(DataBaseEngine):
    def __init__(self, request, response):
        self.listeners = {}

    def on_event(self, event_name, callback):
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)

    def emit(self, event_name, data):
        if event_name in self.listeners:
            for callback in self.listeners[event_name]:
                callback(data)
