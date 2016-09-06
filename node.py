import fingertable
from config import * 
from common import *
# from hashids import Hashids
# hashids = Hashids(min_length=4)
#from hashlib import sha1

class Node(object):
    def __init__(self, ring_id, id, **kwargs):
        """Initialize Node object.
        :params id: ID of Node on Chord Ring
        :params finger: Fingertable object
        :params ip: ip address of real node (physical gateway)
        :params sensors: list of Sensors object
        :params **kwargs: specific args for Node
        :return: class Node
        HOW-TO:
        The simplest way to create a node instance is initialization::
            >> from .node import node
            >> node = node.Node(id=0, 
                                ip=10.0.0.10, 
                                some_needed_args_for_Node)"""

        self.id = id
        self.ring_id = ring_id
        self.finger = []
        self.ip = None
        self.keys = []
        self.successor = None
        self.predecessor = None
        
        #self.initFingerTable()


    def initFingerTable(self,node_old):
        print 'initFingerTable at Node:',self.id
        for i in range(0,HASH_NODE_LEN):
            finger_ = fingertable.Finger(self.id,i)
            self.finger.append(finger_)
        
        self.finger[0].successor = node_old.findSuccessor(self.finger[0].start)
        self.successor = self.finger[0].successor
        self.predecessor =  self.successor.predecessor
        self.successor.predecessor = self
        self.predecessor.successor = self
    
    
    def updateFingerTable(self):
        print self.id,'updateFingerTable'
        for i in range(0,HASH_NODE_LEN):
            self.finger[i].successor = self.findSuccessor(self.finger[i].start)


    def findSuccessor(self,id):
        print 'FindSuccessor of node',id,'at Node',self.id
        if (id is self.id): 
            return self
        if (isInInterval(id,self.id,self.successor.id,False,True)):
            return self.successor
        else:
            n0 = self.closestPrecedingFinger(id)
            succ = n0.findSuccessor(id) 
            print 'findSuccessor return succ:',succ.id
        return succ


    def closestPrecedingFinger(self,id):
        for i in range(HASH_NODE_LEN-1,-1,-1):
            print 'finger.start',self.finger[i].start,'test closest:',self.finger[i].successor
            if ((self.finger[i].successor is not None) and (isInInterval(self.finger[i].successor.id,self.id,id,False,False))):
                return self.finger[i].successor
        return self.successor
    
    def updateOthers(self,node_):
        while (node_ is not self):
            node_.updateFingerTable()
            node_ = node_.successor


    def joinFirst(self):
        for i in range(HASH_NODE_LEN):
            print 'joinFirst:',i,
            finger_ = fingertable.Finger(self.id,i)
            finger_.successor = self
            self.finger.append(finger_)

        self.successor = self.finger[0].successor
        self.predecessor = self

    def join(self,node_old):
        print 'NodeOld:',node_old.id
        self.initFingerTable(node_old)
        self.updateFingerTable()
        self.updateOthers(self.successor)

    def leave(id):
        raise NotImplementedError
    
    def lookup(key):
        node_ = self.findSuccessor(key)
        return node_

    def print_(self):
        print ''
        print 'Node-', self.id
        print '     Ring:', self.ring_id
        print '     Keys:', self.keys
        print '     FingerTable:',
        for fg in self.finger:
            print fg.start,'-',fg.successor.id,'|',