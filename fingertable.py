from config import *
# from hashids import Hashids
# hashids = Hashids(min_length=4)
class Finger(object):
    def __init__(self,node_id, index, successor=None):
        # self.start = hashids.encode((node_id + 2**index) % MAX_NODES)
        self.start = (node_id + 2**index) % MAX_NODES
        self.successor = successor
        self.weight = 1