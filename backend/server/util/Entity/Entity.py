
SOULS_SUPPORTED = ["INORGANIC", "ORGANIC", "DREAMS"]

class Entity():

    def __init__(self, soul="MACHINES", args, kwargs):
        pass

    @property
    def UNIQUE_ID(self):
        pass


class Base(Entity):
    # code up logic for defining this as list of entities
    # or some type of collection, i guess object is the most abstract collection
    def __init__(self, entity_class: Entity, collection_class: object):
        self.collection = collection_class()
        self.history = {}
        pass


    @property
    def UNIQUE_ID(self):
        this_hash = ""
        for e in self.collection:
            this_hash += e.UNIQUE_ID
        
        return this_hash
    
    def add_entity(self, new):
        self.update_history()
        self.collection[new.UNIQUE_ID] = new
        return
    
    def remove_entity(self, e):
        self.update_history()
        # add to archives?
        # make some logic to keep history/logging for research purposes?

        self.collection[e.UNIQUE_ID] = None
        return
    
    def update_history(self):
        # do timestamps with snapshots of self.collection at this point
        self.history[time.now()] = hash(self.collection)
        return
