from dataclasses import dataclass

"""
Thinking maybe have this class to handle any common Flask
Logic that I see in ClientRouter and AdminRouter
"""

@dataclass
class VideoUpload:
    name: str
    bytes: bytes
    user_id: int
    upload_date: str

class Router():
    def __init__(self, app, deployment, orchestrator, request):
        self.orchestrator = orchestrator
        self.request = request
        self.deployment = deployment

        self.set_up()
        self.construct_routes(app, request)



    def set_up(self):
        pass

    def construct_routes(self, app, request):
        pass