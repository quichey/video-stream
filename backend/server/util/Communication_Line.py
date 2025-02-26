PROTOCOLS_SUPPORTED = ["HTTP", "UDP", "TCP", "NEURAL_NET"]
CHORDS_SUPPORTED = []
ENTITIES_SUPPORTED = ["MACHINES", "CELLS", "INSTRUMENTS"]

import socket.socket as Socket
import server.util.Entity.Entity as Entity
import server.util.Entity.Base as Base

class Communication_Line():

    def __init__(self, entity_class: Entity, source_0: Base, source_1: Base, protocol="HTTP"):
        self.entity_to = source_0.UNIQUE_ID
        self.entity_from = source_1.UNIQUE_ID
    
    @property
    def chord_function():
        pass

    @property
    def chord(self, chord_function):
        if self.chord is None:
            self.chord = chord_function()
        return self.chord

    @property
    def entity_to(self):
        return self.entity_to
    @property
    def entity_from(self):
        return self.entity_from

    def send_message(self, giver, receiver):
        pass



class INTERNET_CONNECTION(Communication_Line):
    
    @property
    def chord(self):
        return self.chord
    @property
    def socket(self):
        return self.chord

    @property
    def entity_to(self):
        return self.entity_to
    @property
    def ip_addr_to(self):
        return self.ip_addr_to

    @property
    def entity_from(self):
        return self.entity_from
    @property
    def ip_addr_from(self):
        return self.ip_addr_to

"""
These classes below were just musings of my current personal hobbies/disciplines
Bodybuilding and music
Body and Mind
Heart and Will
Heart and Soul gives fruition to the future I long to live

Dichotomies Give Birth to Trichotomies
"""

class MUSCLE_FIBER(Communication_Line):
    @property
    def will_to():
    
    @property
    def will_from():


class MELODY(Communication_Line):
    @property
    def heart_to():

    def heart_from():
