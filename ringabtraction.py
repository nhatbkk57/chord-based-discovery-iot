import config
import hashlib
from common import *
#from .node import node
class Ring(object):
    def __init__(self,ringID):
        self.ringID = ringID
        self.successor = None
        self.predecessor = None
        self.fingertable = []