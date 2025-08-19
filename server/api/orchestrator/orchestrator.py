from api.orchestrator.session.SessionManagement import SessionManagement
from api.orchestrator.Cache.Cache import Cache


class Orchestrator():
    SESSION_MANAGEMENT = SessionManagement()
    CACHE = Cache()
    def __init__(self):
        pass

    def handle_request(self, request):
        use_cache = pass
        if use_cache:
            result = self.CACHE.get_data(request)
        else:
            result = self.SESSION_MANAGEMENT.on_request(request)
        
        cache_result = pass
        if cache_result:
            self.Cache.cache_data(request, result)

        return result