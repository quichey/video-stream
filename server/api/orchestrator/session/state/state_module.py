from sqlalchemy import create_engine

from api.util.db_engine import DataBaseEngine
from db.Schema import database_specs, database_specs_cloud_sql, Base
#from api.Cache.SessionManagement import SessionManagement

class StateModule(DataBaseEngine):
    STORAGE = None
    def __init__(self, request, response, storage, deployment, *args, **kwargs):
        super().__init__(deployment, *args, **kwargs)
        self.STORAGE = storage
        self.listeners = {}

    def on_event(self, event_name, callback):
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)

    def emit(self, event_name, data):
        if event_name in self.listeners:
            for callback in self.listeners[event_name]:
                callback(data)
