import config
import hashlib
from common import *
#from .node import node
class Ring(object):
    def __init__(self,id,**kwargs):
        self.id = id
        self.ringsize = config.MAX_NODES
        self.nodes = []

    def print_(self):
        #self.nodes.sort()
        print 'Ring[',self.id,']:'
        print 'Nodes:',
        for n in self.nodes:
            print n.id,
    
    def create_(self):
        # self.nodes[2].id = 3
        # self.nodes[3].id = 4
        if (len(self.nodes) > 0):
            self.nodes[0].joinFirst(self.id)
            len_node = len(self.nodes)
        # print 'test=',isInInterval(3,7,1,False,True)
        # print ''
            if (len_node > 1):
                for i in range(1,len_node):
                    self.nodes[i].join(self.nodes[i-1])

        

        #self.nodes[2].join(self.nodes[1])
        #self.nodes[2].print_()