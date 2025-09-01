from api.orchestrator.session.SessionManagement import SessionManagement
from api.orchestrator.Cache.Cache import Cache
from api.orchestrator.storage.storage import Storage
from api.orchestrator.storage.local_storage import LocalStorage


class Orchestrator():
    SESSION_MANAGEMENT = None
    CACHE = None
    DEPLOYMENT = None
    def __init__(self, deployment):
        self.DEPLOYMENT = deployment
        if deployment == 'local':
            self.STORAGE = LocalStorage()
        else:
            self.STORAGE = Storage()
        self.SESSION_MANAGEMENT = SessionManagement(deployment, self.STORAGE)
        self.CACHE = Cache()

    def handle_request(self, request, response):
        use_cache = False
        if use_cache:
            result = self.CACHE.get_data(request, response)
        else:
            result = self.SESSION_MANAGEMENT.on_request(request, response)
        
        cache_result = False
        if cache_result:
            self.Cache.cache_data(request, result)

        #TODO: have ways for AdminRoutes.py to interact?

        return response