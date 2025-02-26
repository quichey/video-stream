ENGINE_SUPPORTED = ["MYSQL"]

class Address():

    def __init__(self, host, port, engine="MYSQL"):
        self.host = host
        self.port = port

    @property
    def host(self):
        return self.host

    @property
    def port(self):
        return self.port