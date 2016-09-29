from config import *
from common import *

class Sensor(object):
    def __init__(self,nodeID,sensorID):
        key_ = hashKey(nodeID,sensorID)
        self.sensorID = sensorID
        self.nodeID = nodeID
        self.status = True
        self.keyID = key_