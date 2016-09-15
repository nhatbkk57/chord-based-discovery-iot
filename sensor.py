from config import *
from common import *

class Sensor(object):
    def __init__(self,ringID,nodeID,sensorID):
        key_ = hashKey(ringID,nodeID,sensorID)
        self.sensorID = sensorID
        self.nodeID = nodeID
        self.status = True
        self.id = key_
        self.key = str(key_)