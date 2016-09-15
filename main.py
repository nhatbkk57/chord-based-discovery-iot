import config
import ring
import node
import sensor
import sys
import random
import json
from common import *

rings = []
nodes = []
sensors = []
json_ = []

def generate_rings(num_rings):
    for i in range(0, num_rings):
        ring_ = ring.Ring(i)
        ring_.id = 1
        # print "new ring:", ring_
        rings.append(ring_)

def generate_nodes(num_nodes):
    if (len(rings) == 1):
        list_id = random.sample(range(0, LIMIT_NODE), num_nodes)
        for i in list_id:
            new_node = node.Node(rings[0].id,i)
            nodes.append(new_node)
            rings[0].nodes.append(new_node)
            # print 'Node_ChordKey:',new_node.id
    else:
        raise NotImplementedError

def generate_sensors(num_sensors):
    list_id = random.sample(range(1, LIMIT_SENSOR), num_sensors)
    for i in list_id:
        lenListNode = len(nodes)
        node_ = nodes[random.randint(0,lenListNode-1)]
        # print 'Sensor_Connect_To_NodeID:', node_.nodeID
        sensorID = i
        sensor_ = sensor.Sensor(node_.ringID,node_.nodeID,sensorID)
        sensors.append(sensor_)
        node_.connectSensors.append(sensor_)
        info_ = {'NodeID':sensor_.nodeID, 'SensorID':sensor_.sensorID}
        node_.insert(sensor_.id,info_)


def print_():
    for node_ in rings[0].nodes:
            jsonNODE = node_.print_()
            json_.append(jsonNODE)
    return json.dumps(json_,indent=4, sort_keys=True) 

def gen_env(numring,numnode,numsensor):
    generate_rings(numring)
    generate_nodes(numnode)
    rings[0].create_()
    generate_sensors(numsensor)
    return True
   

def lookup(nodeID,keyID):
    node_ = get_node_byID(nodes,nodeID)
    result = node_.lookup(keyID)
    return json.dumps(result,indent=4, sort_keys=True) 

def main(argv):
    num_rings = int(argv[0])
    num_nodes = int(argv[1])
    num_sensors = int(argv[2])
    print 'Number of rings:', num_rings
    print 'Number of nodes:', num_nodes
    generate_rings(num_rings)
    generate_nodes(num_nodes)
    rings[0].create_()
    generate_sensors(num_sensors)

    for node_ in rings[0].nodes:
            jsonNODE = node_.print_()
            json_.append(jsonNODE)
    
    print json.dumps(json_,indent=4, sort_keys=True)
            
    # print_()
    
    # nodes[3].print_()
    # nn = nodes[10]
    # nn.id = 300
    # nodes[10].print_()
    


if __name__ == "__main__":
   main(sys.argv[1:])

