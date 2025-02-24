import os
import util

root_prefix = "QUEUE_"

class Queue():
    list_name = None
    
    def __init__(self, product):
        self.list_name = f"{root_prefix}_{product}"
        util.set_env(self.list_name,"")

    @property
    def product_list(self):
        _list = util.get_env(self.list_name)
        _list = # however to convert string of comma delimited to python list
        return _list

    def add(self, node):
        self.product_list.append(node)
        env_list = # however convert python list to comma string
        util.set_env(self.list_name, env_list)

    def get(self, node):
        for idx, curr_node in enumerate(self.product_list):
            if curr_node == node:
                return idx
        raise Exception("item not found")