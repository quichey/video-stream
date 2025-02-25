class MACHINE(Entity):

    def __init__(self, soul="INORGANIC", host, port, engine):
        self.host = host
        self.port = port

    @property
    def UNIQUE_ID(self):
        return {"host": self.host, "port": self.port}
    
    @property
    def host(self):
        return self.host
    
    @property
    def port(self):
        return self.port
    
    @property
    def hash(self):
        return f"{self.host}_{self.port}"

class WEB_BROWSER(MACHINE):
    def __init__(self, engine="CHROME"):
        pass


class DATABASE(MACHINE):

    def __init__(self, engine="MYSQL"):
        pass



class DATA_VERSE(Base):
    def __init__(self):
        self.super(entity_class=DATABASE)
    
    @override
    def add_entity(self, e)
        # adding a database to collections of databases
        pass

    def update_state():
        pass

class CLIENT_BASE(DATA_VERSE):
    def blah():
        pass
