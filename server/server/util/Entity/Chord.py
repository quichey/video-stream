class CHORD(Entity):
    
    def is_active(self):
        return self.is_active
    
    def activate(self):
        pass
    
    def deactivate(self):
        pass

class PROTOCOL(CHORD):
    pass

class Message(Entity):
    MESSAGES_SUPPORTED = ["PUBLIC", "PRIVATE"]
    def __init__(self, message_type):
        self.message_type = message_type