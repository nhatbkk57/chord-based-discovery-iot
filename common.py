from config import *

# def get_node_byID(nodes,id):
#     length = len(nodes)
#     for n in nodes:
#         if (n.id == id):
#             n.id = 500
#             return n
#     return None

def isInInterval(val,left,right,equal_left,equal_right):
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