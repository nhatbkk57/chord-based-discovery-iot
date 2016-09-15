from config import *
import hashlib
import zlib
def get_node_byID(nodes,id):
    for n in nodes:
        if (n.nodeID == id):
            return n
    return None

def isInInterval(val,left,right,equal_left,equal_right):
    # print "Test:",left,right,equal_left,equal_right
    if (equal_left and val == left):
        return True

    if (equal_right and val == right):
        return True

    if (right > left):
        if (val > left and val < right):
            return True
        else:
            return False
    
    if (right < left):
        if (val < left):
            left = left - MAX_NODES
        else:
            if (val > left):
                right = right + MAX_NODES

        if (val >left and val < right):
            return True
        else:
            return False
    #if left = right
    return True

    # if (equal_left and val == left):
    #     return True

    # if (equal_right and val == right):
    #     return True

    # if (right > left):
    #     if (val > left and val < right):
    #         return True
    
    # if (right < left):
    #     if (val < left and val < right):
    #         return True
    
    # if (right == left):
    #     return True
    
    # return False

########### HASHING ###########

# def hashKey(ringID,nodeID,sensorID):
#     if (sensorID == 0):
#         sensorID = ''
#         for i in range(HASH_SENSOR_LEN):
#             sensorID = sensorID + '0'
#         binKey = '0b' + '{0:04b}'.format(nodeID + 7) + sensorID
#     else:
#         binKey = '0b' + '{0:04b}'.format(nodeID + 7) + '{0:04b}'.format(sensorID)
#     intKey = int(binKey,2) % (2 ** M)
#     return intKey


def hashKey(ringID,nodeID,sensorID):
    #md5
    md5 = hashlib.md5()
    #sha1
    sha1 = hashlib.sha1()

    str_ = str(nodeID)+str(sensorID)
    sha1.update(str_)
    intkey = int(sha1.hexdigest(),16)
    if (sensorID == 0):
        print "NodeID =",nodeID,"- HashKey =",intkey
    else:
        print "NodeID =",nodeID,"SensorID =",sensorID,"- HashKey =",intkey
    return intkey