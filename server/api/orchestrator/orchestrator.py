from api.orchestrator.session.SessionManagement import SessionManagement
from api.orchestrator.Cache.Cache import Cache


class Orchestrator:
    SESSION_MANAGEMENT = None
    CACHE = None

    def __init__(self):
        self.SESSION_MANAGEMENT = SessionManagement()
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

        # TODO: have ways for AdminRoutes.py to interact?

        return response
