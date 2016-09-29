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
    print "numring:",num_rings
    for i in range(0, num_rings):
        ring_ = ring.Ring(i)
        # print "new ring:", ring_
        rings.append(ring_)

def generate_nodes(num_nodes):
    list_id = random.sample(range(0, LIMIT_NODE), num_nodes)
    for i in list_id:
            new_node = node.Node(i)
            nodes.append(new_node)
            ringIndex =  random.randint(0,len(rings)-1)
            rings[ringIndex].nodes.append(new_node)

def generate_sensors(num_sensors):
    list_id = random.sample(range(1, LIMIT_SENSOR), num_sensors)
    for i in list_id:
        lenListNode = len(nodes)
        node_ = nodes[random.randint(0,lenListNode-1)]
        # print 'Sensor_Connect_To_NodeID:', node_.nodeID
        sensorID = i
        sensor_ = sensor.Sensor(node_.nodeID,sensorID)
        sensors.append(sensor_)
        node_.connectSensors.append(sensor_)
        info_ = {'NodeID':sensor_.nodeID, 'SensorID':sensor_.sensorID}
        node_.insert(sensor_.keyID,info_)


def print_():
    json_ = []
    for ring_ in rings:
        jsonRING = {"1_RingID":ring_.id,"2_Nodes":[]}
        for node_ in ring_.nodes:
            jsonNODE = node_.print_()
            jsonRING["2_Nodes"].append(jsonNODE)
        json_.append(jsonRING)
    return json.dumps(json_,indent=4, sort_keys=True) 

def gen_env(numring,numnode,numsensor):
    generate_rings(numring)
    generate_nodes(numnode)
    for ring_ in rings:
        ring_.create_()
    generate_sensors(numsensor)

    for ring_ in rings:
        print "Ring:",ring_.id
        print "Node"
        for node_ in ring_.nodes:
            print node_.nodeID,
        print ""
    return True
   

def lookup(nodeID,keyID):
    node_ = get_node_byID(nodes,nodeID)
    tracking = None
    result = node_.lookup(keyID,tracking)
    if (result is None):
        return json.dumps("Not Found")
    else:
        return json.dumps(result,indent=4, sort_keys=True)

def insert(nodeID,sensorID):
    node_ = get_node_byID(nodes,nodeID)
    sensor_ = sensor.Sensor(node_.ringID,node_.nodeID,sensorID)
    sensors.append(sensor_)
    node_.connectSensors.append(sensor_)
    info_ = {'NodeID':sensor_.nodeID, 'SensorID':sensor_.sensorID}
    node_.insert(sensor_.id,info_)
    return sensor_.key

def join(nodeID,nodeOld):
    node_ = get_node_byID(nodes,nodeID)
    nodeOld_ = get_node_byID(nodes,nodeOld)
    node_.join(nodeOld_)
    return True


def test1():
    ### 2 ring have 1 same node 
    node_ = rings[0].nodes[0]
    nodeOld_ = rings[1].nodes[0]
    node_.join(nodeOld_)
    print "Node",node_.nodeID,"Join By NodeOld",nodeOld_.nodeID
    
    if (len(rings[0].nodes[0].connectSensors)):
        keyID = rings[0].nodes[0].connectSensors[0].keyID
    else:
        keyID = rings[0].nodes[1].connectSensors[0].keyID
    node_ = rings[1].nodes[1]
    print "Node",node_.nodeID,"Look Up Key",keyID,"which connect to Node",rings[0].nodes[0].nodeID
    tracking = None
    result = node_.lookup(keyID,tracking)
    print json.dumps(tracking,indent=4, sort_keys=True)
    if (result is None):
        return json.dumps("Not Found")
    else:
        return json.dumps(result,indent=4, sort_keys=True)

def test2():
    ### 3 ring have 1 same node
    node0_ = rings[0].nodes[0]
    nodeOld1_ = rings[1].nodes[0]
    node0_.join(nodeOld1_)
    print "Node",node0_.nodeID,"Join By NodeOld",nodeOld1_.nodeID
    nodeOld2_ = rings[2].nodes[0]
    node0_.join(nodeOld2_)
    print "Node",node0_.nodeID,"Join By NodeOld",nodeOld2_.nodeID
    
    if (len(rings[0].nodes[0].connectSensors)):
        keyID = rings[0].nodes[0].connectSensors[0].keyID
    else:
        keyID = rings[0].nodes[1].connectSensors[0].keyID
    node_ = rings[2].nodes[2]
    print "Node",node_.nodeID,"Look Up Key",keyID,"which connect to Node",rings[0].nodes[0].nodeID
    tracking = None
    result = node_.lookup(keyID,tracking)
    print json.dumps(tracking,indent=4, sort_keys=True)
    if (result is None):
        return json.dumps("Not Found")
    else:
        return json.dumps(result,indent=4, sort_keys=True)

def test3():
    ### 3 ring: ring 0,1 have 1 same node; ring 1,2 have 1 same node; lookup key of ring 0 at ring 2
    node0_ = rings[0].nodes[0]
    nodeOld1_ = rings[1].nodes[0]
    node0_.join(nodeOld1_)
    print "Node",node0_.nodeID,"Join By NodeOld",nodeOld1_.nodeID
    node1_ = rings[1].nodes[1]
    nodeOld2_ = rings[2].nodes[0]
    node1_.join(nodeOld2_)
    print "Node",node1_.nodeID,"Join By NodeOld",nodeOld2_.nodeID

    if (len(rings[0].nodes[0].connectSensors)):
        keyID = rings[0].nodes[0].connectSensors[0].keyID
    else:
        keyID = rings[0].nodes[1].connectSensors[0].keyID
    node_ = rings[2].nodes[2]
    print "Node",node_.nodeID,"Look Up Key",keyID,"which connect to Node",rings[0].nodes[0].nodeID
    tracking = None
    result = node_.lookup(keyID,tracking)
    print json.dumps(tracking,indent=4, sort_keys=True)
    if (result is None):
        return json.dumps("Not Found")
    else:
        return json.dumps(result,indent=4, sort_keys=True)

def main(argv):
    num_rings = int(argv[0])
    num_nodes = int(argv[1])
    num_sensors = int(argv[2])
    print 'Number of rings:', num_rings
    print 'Number of nodes:', num_nodes
    generate_rings(num_rings)
    generate_nodes(num_nodes)
    for ring_ in rings:
        ring_.create_()
    generate_sensors(num_sensors)

    for node_ in nodes:
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

