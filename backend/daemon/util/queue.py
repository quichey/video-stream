import os
import util

root_prefix = "QUEUE_"

class Queue():
    
    def __init__(product):
        util.set_env(f"{root_prefix}_{product}","")

    def add(self, node):
        pass

    def get(self, node):
        pass