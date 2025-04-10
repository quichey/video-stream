"""
Thinking maybe have this class to handle any common Flask
Logic that I see in ClientRouter and AdminRouter
"""

class Router():
    def __init__(self, app, cache, request):
        self.cache = cache
        self.request = request

        self.set_up()
        self.construct_routes(app, request)
    

    def extract_user_info(self):
        form_data = json.loads(request.data)
        # TODO: change later to something like request.form['username']
        user_info = {
            "id": form_data['user_id'],
            "name": form_data['user_name']
        }
        return user_info

    

    def set_up(self):
        pass

    def construct_routes(self, app, request):
        pass