import fingertable
import sensor
from config import * 
from common import *
import json
# from hashids import Hashids
# hashids = Hashids(min_length=4)
#from hashlib import sha1

path = []

class Node(object):
    def __init__(self, ringID, nodeID, **kwargs):
        """Initialize Node object.
        :params nodeID: Private ID of Physical Device - Node
        :params ringID: ID of ring
        :params id: identifier on chord ring of Node
        :params finger: Fingertable object
        :params ip: ip address of real node (physical gateway)
        :params connectSensors: list of Sensors which connect directly to Node
        :params manageInforSensors: list of Sensors which Node responsible
        :params status: status of Node (failed/left = False, active = True)
        :params **kwargs: specific args for Node
        :return: class Node
        HOW-TO:
        The simplest way to create a node instance is initialization::
            >> from .node import node
            >> node = node.Node(RingID,nodeID)"""

        self.nodeID = nodeID 
        self.ringID = ringID
        self.id = hashKey(ringID,nodeID,0)
        self.finger = []
        self.ip = None
        self.connectSensors = []
        self.manageInfoSensors = []
        self.status = True
        self.successor = None
        self.predecessor = None

        
        #self.initFingerTable()


    def initFingerTable(self,node_old):
        # print 'initFingerTable at Node:',self.id
        for i in range(0,M):
            finger_ = fingertable.Finger(self.id,i)
            self.finger.append(finger_)
        
        self.finger[0].successor = node_old.findSuccessor(self.finger[0].start)
        self.successor = self.finger[0].successor
        self.predecessor =  self.successor.predecessor
        self.successor.predecessor = self
        self.predecessor.successor = self
    
    
    def updateFingerTable(self):
        # print self.id,'updateFingerTable'
        for i in range(0,M):
            self.finger[i].successor = self.findSuccessor(self.finger[i].start)


    def findSuccessor(self,id):
        # print 'FindSuccessor of node',id,'at Node',self.id
        # print
        path.append(self.nodeID) 
        if (id == self.id): 
            return self
        if (isInInterval(id,self.id,self.successor.id,False,True)):
            return self.successor
        else:
            n0 = self.closestPrecedingFinger(id)
            succ = n0.findSuccessor(id) 
            # print 'findSuccessor return succ:',succ.id
        return succ


    def closestPrecedingFinger(self,id):
        for i in range(M-1,-1,-1):
            # print 'finger.start',self.finger[i].start,'test closest:',self.finger[i].successor
            if ((self.finger[i].successor is not None) and (isInInterval(self.finger[i].successor.id,self.id,id,False,False))):
                return self.finger[i].successor
        return self.successor
    
    def updateOthers(self,node_):
        while (node_ is not self):
            node_.updateFingerTable()
            node_ = node_.successor


    def joinFirst(self):
        for i in range(M):
            # print 'joinFirst:',i,
            finger_ = fingertable.Finger(self.id,i)
            finger_.successor = self
            self.finger.append(finger_)

        self.successor = self.finger[0].successor
        self.predecessor = self

    def join(self,node_old):
        # print 'NodeOld:',node_old.id
        self.initFingerTable(node_old)
        self.updateFingerTable()
        self.updateOthers(self.successor)

    def leave(self):
        self.successor.predecessor = self
        self.predecessor.successor = self.successor
        ## self.moveSensorInfo()
        self.status = False
        
    def lookup(self,key):
        global path
        path = []
        node_ = self.findSuccessor(key)
        for sensor_ in node_.manageInfoSensors:
            if (sensor_['key'] == key):
                json_ = {'info':sensor_['info'], 'path':path}
                return json_
        return None

    def insert(self,key,value):
        # print "Insert Key: ",key
        node_ = self.findSuccessor(key)
        info = {'key':key,'info':value}
        node_.manageInfoSensors.append(info)

    # def move(self,succ,key):


    def print_(self):
        jsonNODE = {}
        jsonNODE["1_KeyID"] = self.id
        jsonNODE["2_NodeID"] = self.nodeID
        jsonNODE["3_RingID"] = self.ringID
        jsonNODE["4_ConnectSensors"] = {"1_Nums":len(self.connectSensors),"2_List":[]}
        jsonNODE["5_ManageSensors"] = {}
        jsonNODE["5_ManageSensors"]["1_Nums"] = len(self.manageInfoSensors)
        jsonNODE["5_ManageSensors"]["2_List"] = self.manageInfoSensors 
        jsonNODE["6_FingerTable"] = []
        # print ''
        # print 'Node-', self.id
        # print '     NodeID:', self.nodeID
        # print '     RingID:', self.ringID
        # print '     Connected Sendor:'
        for ss in self.connectSensors:
            jsonSS = {"SensorID":ss.sensorID,"SensorKey":ss.key}
            jsonNODE['4_ConnectSensors']['2_List'].append(jsonSS)
            # print 'SensorID:',ss.sensorID,'-','ChordKey:',ss.key
        # print '     Manage Info Sendor:'
        # json_ = json.loads(self.manageInfoSensors)
        # print json.dumps(self.manageInfoSensors,indent=4, sort_keys=True)
        # print '     FingerTable:'
        for fg in self.finger:
            jsonFG = str(fg.start) + '-' + str(fg.successor.id)
            jsonNODE['6_FingerTable'].append(jsonFG)
            # print '|',fg.start,'-',fg.successor.id,'|'
        return jsonNODE