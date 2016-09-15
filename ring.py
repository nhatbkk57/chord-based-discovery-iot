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
        self.nodes[0].joinFirst()
        len_node = len(self.nodes)
        # print 'test=',isInInterval(3,7,1,False,True)
        # print ''
        for i in range(1,len_node):
            self.nodes[i].join(self.nodes[i-1])

        

        #self.nodes[2].join(self.nodes[1])
        #self.nodes[2].print_()