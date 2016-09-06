import fingertable
from config import * 
from common import *
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

    def findSuccessor(self,id):
        print 'FindSuccessor of node',id,'at Node',self.id
        if (id is self.id):
            return self
        else:
            node_ = self.findPredecessor(id)
            return node_.successor
    
    def findPredecessor(self,id):
        node_ = self
        while(not isInInterval(id,node_.id,node_.successor.id,True,True)):
            node_ = node_.closestPrecedingFinger(id)
        print 'findPredecessor return Node_New:',node_.id
        return node_

    def closestPrecedingFinger(self,id):
        for i in range(HASH_NODE_LEN-1,-1,-1):
            print 'finger.start',self.finger[i].start,'test closest:',self.finger[i].successor.id
            if ((isInInterval(self.finger[i].successor.id,self.id,id,False,True))):
                return self.finger[i].successor
        return self

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
        # self.updateFingerTable()
        self.updateOthers()

    def initFingerTable(self,node_old):
        print 'initFingerTable at Node:',self.id
        for i in range(0,HASH_NODE_LEN):
            finger_ = fingertable.Finger(self.id,i)
            self.finger.append(finger_)
        
        #find first line in fingertable and successor, predecessor

        self.finger[0].successor = node_old.findSuccessor(self.finger[0].start)
        self.successor = self.finger[0].successor
        self.predecessor =  self.successor.predecessor
        self.successor.predecessor = self
        self.predecessor.successor = self
        print 'init first finger = ',self.successor.id

        #update last fingertable's lines
        print 'init last fingertable line:'
        for i in range(0,HASH_NODE_LEN-1):
            if (isInInterval(self.finger[i+1].start,self.id,self.finger[i].successor.id,True,True)):
                self.finger[i+1].successor = self.finger[i].successor
                print 'init finger',self.finger[i+1].start,'=',self.finger[i+1].successor.id 
            else:
                self.finger[i+1].successor = node_old.findSuccessor(self.finger[i+1].start)
                print 'init finger',self.finger[i+1].start,'=',self.finger[i+1].successor.id
    
    def updateOthers(self):
        # while (node_ is not self):
        #     node_.updateFingerTable()
        #     node_ = node_.successor
        for i in range(0,HASH_NODE_LEN):
            pred_ = ((self.id - 2 ** i) + MAX_NODES) % MAX_NODES
            print 'updateOthers check=',pred_
            if (self.predecessor.id is pred_):
                p = self.predecessor
            else:
                p = self.findPredecessor(pred_)
            print self.id,'updateOthers at pred_=',p.id
            p.updateFingerTable(self,i);

    def updateFingerTable(self,Node_S,i):
        print self.id,'updateFingerTable with Node_S=',Node_S.id
        # for i in range(0,HASH_NODE_LEN):
        #     self.finger[i].successor = self.findSuccessor(self.finger[i].start)

        if (isInInterval(Node_S.id, self.id, self.finger[i].successor.id, False, False)):
            self.finger[i].successor = Node_S
            print 'updated finger-',i,'.successor=',self.finger[i].successor.id
            p = self.predecessor
            p.updateFingerTable(Node_S,i)

    def leave(id):
        raise NotImplementedError
    
    def lookup(key):
        if (key in self.keys):
            return self.id
        else:
            raise NotImplementedError

    def print_(self):
        print ''
        print 'Node-', self.id
        print '     Ring:', self.ring_id
        print '     Keys:', self.keys
        print '     FingerTable:',
        for fg in self.finger:
            print fg.start,'-',fg.successor.id,'|',