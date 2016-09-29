import fingertable
import sensor
import ringabtraction
from config import * 
from common import *
import json
import random
# from hashids import Hashids
# hashids = Hashids(min_length=4)
#from hashlib import sha1

path = []
firstlookup = None

class Node(object):
    def __init__(self, nodeID, **kwargs):
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
        self.rings = [] 
        self.keyID = hashKey(nodeID,0)
        self.connectSensors = []
        self.keysManager = []
        self.status = True


    def initFingerTable(self,node_old):
        # print 'initFingerTable at Node:',self.keyID
        ring_ = ringabtraction.Ring(node_old.rings[0].ringID)
        self.rings.append(ring_)
        # print "Node",self.nodeID,"Init Ring",ring_.ringID
        for i in range(0,M):
            finger_ = fingertable.Finger(self.keyID,i)
            ring_.fingertable.append(finger_)
        
        ring_.fingertable[0].successor = node_old.findSuccessor(ring_.ringID,ring_.fingertable[0].start)
        ring_.successor = ring_.fingertable[0].successor
        ring_.predecessor = ring_.successor.get_ring_byID(ring_.ringID).predecessor
        ring_.successor.get_ring_byID(ring_.ringID).predecessor = self
        ring_.predecessor.get_ring_byID(ring_.ringID).successor = self
    
    
    def updateFingerTable(self,ringID):
        # print self.keyID,'updateFingerTable'
        ring_ = self.get_ring_byID(ringID)
        for i in range(0,M):
            # print "finger",i
            ring_.fingertable[i].successor = self.findSuccessor(ringID,ring_.fingertable[i].start)


    def findSuccessor(self,ringID,keyID,**kwargs):
        # print 'FindSuccessor of node',id,'at Node',self.keyID
        # print "ringID=",ringID
        if (len(kwargs)):
            step = {"Node":self.nodeID,"Task":"Find Successor Of Key"}
            tracking = kwargs["tracking"]
            tracking["trackNodes"].append(step)
        ring_ = self.get_ring_byID(ringID)

        if (keyID == self.keyID): 
            # print "Node",self.nodeID,"found succ of key is self",self.nodeID
            return self
        # print "nodeID=",self.nodeID,"find ringID=", ringID
        if (isInInterval(keyID,self.keyID,ring_.successor.keyID,False,True)):
            # print "Node",self.nodeID,"found succ of key is Node",ring_.successor.nodeID
            return ring_.successor
        else:
            node_ = self.closestPrecedingFinger(ringID,keyID)
            if (len(kwargs)):
                tracking = kwargs["tracking"]
                succ = node_.findSuccessor(ringID,keyID,tracking=tracking)
            else:
                succ = node_.findSuccessor(ringID,keyID) 
            # print 'findSuccessor return succ:',succ.id
            return succ


    def closestPrecedingFinger(self,ringID,keyID):
        ring_ = self.get_ring_byID(ringID)
        ### Look up FingerTable from bottom to top for getting Closest Predecessor
        for i in range(M-1,-1,-1):
            # print 'finger.start',ring_.fingertable[i].start,'test closest:',ring_.fingertable[i].successor
            if ((ring_.fingertable[i].successor is not None) and (isInInterval(ring_.fingertable[i].successor.keyID,self.keyID,keyID,False,False))):
                return ring_.fingertable[i].successor
        return ring_.successor
    
    def updateOthers(self,ringID,node_):
        while (node_ is not self):
            node_.updateFingerTable(ringID)
            ring_ = node_.get_ring_byID(ringID)
            node_ = ring_.successor


    def joinFirst(self,ringID):
        ring_ = ringabtraction.Ring(ringID)
        ### Init FingerTable
        for i in range(M):
            # print 'joinFirst:',i,
            finger_ = fingertable.Finger(self.keyID,i)
            finger_.successor = self
            ring_.fingertable.append(finger_)
        ring_.successor = ring_.fingertable[0].successor
        # print "Node",self.nodeID,"join First with succNode",ring_.successor.nodeID
        ring_.predecessor = self
        self.rings.append(ring_)


    ### Node join with a known Node
    def join(self,node_old):
        # print 'NodeID=', self.nodeID,"Join By Node",node_old.nodeID
        self.initFingerTable(node_old)
        ring_ = self.get_ring_byID(node_old.rings[0].ringID)
        # print "nodeID=",self.nodeID
        self.updateFingerTable(ring_.ringID)
        self.updateKeysManager()
        self.updateOthers(ring_.ringID,ring_.successor)

    def leave(self):
        for ring_ in self.rings:
            ring_.successor.get_ring_byID(ring_.ringID).predecessor = self
            ring_.predecessor.get_ring_byID(ring_.ringID).successor = ring_.successor
        ## self.moveSensorInfo()
        self.status = False
        
    def lookup(self,key,tracking):
        json_ = None
        for sensor_ in self.keysManager:
            if (sensor_['keyID'] == key):
                json_ = {'info':sensor_['info'], 'path':tracking}
                print "Got Sensor Info", json_
                return json_

        print "At Node", self.nodeID, "Look up Key"
        if (tracking is None):
            tracking = {}
            tracking["trackNodes"] = []
            tracking["checkRings"] = []
        step = {"Node":self.nodeID,"Task":"Look Up Key"}
        tracking["trackNodes"].append(step)
        ### Check if key in Node's own Ring???
        for ring_ in self.rings:
            print "Check Ring",ring_.ringID
            listCheckRingsID = []
            for checkRing in tracking["checkRings"]:
                listCheckRingsID.append(checkRing["ringID"])
            print "ListCheckRingsID",listCheckRingsID
            if (ring_.ringID not in listCheckRingsID):
                ### Append new Element into checkRings list for determining end of looking up loop
                checkRing_ = {"ringID":ring_.ringID,"firstNodeLookup":self.nodeID}
                tracking["checkRings"].append(checkRing_)
                ### Find Successor of keyID
                print "At Node", self.nodeID, "FindSuccessor at Ring",ring_.ringID
                node_ = self.findSuccessor(ring_.ringID,key,tracking=tracking)
                print "Found Successor Key at Node",node_.nodeID

                ### Check if keyID in keysManager
                print "Key",key
                for sensor_ in node_.keysManager:
                    print "KeyValue",sensor_['keyID']
                    if (sensor_['keyID'] == key):
                        json_ = {'Info':sensor_['info'],'NumberOfSteps':len(tracking["trackNodes"]),'Steps':tracking["trackNodes"]}
                        print "Found", json_
                        return json_
            
        ### If not found, ask successor lookup
        for ring_ in self.rings:
            for checkRing in tracking["checkRings"]:
                if (ring_.ringID is checkRing["ringID"]):
                    succ_ = ring_.successor
                    ### Check if looking up loop is not completed 
                    print "checkRing",checkRing
                    if (succ_.nodeID is not checkRing["firstNodeLookup"]):
                        ### Send request Look up to successor
                        json_ = succ_.lookup(key,tracking)
                        ### Check if found key
                        if (json_ is not None):
                            ### Return result
                            return json_

    def insert(self,keyID,value):
        # print "Insert Key: ",key
        for ring_ in self.rings:
            node_ = self.findSuccessor(ring_.ringID,keyID)
            keyvalue_ = {'keyID':keyID,'info':value}
            node_.keysManager.append(keyvalue_)

    # def move(self,succ,key):

    def updateKeysManager(self):
        for ring_ in self.rings:
            for key_ in ring_.successor.keysManager:
                if  (isInInterval(key_["keyID"],0,self.keyID,False,True)):
                    self.keysManager.append(key_)
                    ring_.successor.keysManager.remove(key_)


    def print_(self):
        jsonNODE = {}
        jsonNODE["1_KeyID"] = self.keyID
        jsonNODE["2_NodeID"] = self.nodeID
        jsonNODE["3_Rings"] = []
        for ring_ in self.rings:
            jsonNODE["3_Rings"].append(ring_.ringID)
        jsonNODE["4_ConnectSensors"] = {"1_Nums":len(self.connectSensors),"2_List":[]}
        jsonNODE["5_KeysManager"] = {}
        jsonNODE["5_KeysManager"]["1_Nums"] = len(self.keysManager)
        jsonNODE["5_KeysManager"]["2_List"] = self.keysManager 
        jsonNODE["6_FingerTable"] = []
        # print ''
        # print 'Node-', self.keyID
        # print '     NodeID:', self.nodeID
        # print '     RingID:', self.ringID
        # print '     Connected Sendor:'
        for ss in self.connectSensors:
            jsonSS = {"SensorID":ss.sensorID,"SensorKey":ss.keyID}
            jsonNODE['4_ConnectSensors']['2_List'].append(jsonSS)
            # print 'SensorID:',ss.sensorID,'-','ChordKey:',ss.key
        # print '     Manage Info Sendor:'
        # json_ = json.loads(self.manageInfoSensors)
        # print json.dumps(self.manageInfoSensors,indent=4, sort_keys=True)
        # print '     FingerTable:'
        for ring_ in self.rings:
            jsonFGT = {"1_Ring":ring_.ringID,"2_FingerTable":[]}
            for fg in ring_.fingertable:
                # print "FingerStart",fg.start
                jsonFG = str(fg.start) + '-' + str(fg.successor.keyID)
                jsonFGT['2_FingerTable'].append(jsonFG)
                # print '|',fg.start,'-',fg.successor.id,'|'
            jsonNODE["6_FingerTable"].append(jsonFGT)
        return jsonNODE

    def get_ring_byID(self,ringID):
        for ring in self.rings:
            if (ring.ringID == ringID):
                return ring