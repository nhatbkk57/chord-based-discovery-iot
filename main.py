import config
import ring
import node
import sys
import random
from common import *

rings = []
nodes = []

def generate_rings(num_rings):
    for i in range(0, num_rings):
        ring_ = ring.Ring(i)
        ring_.id = 1
        print "new ring:", ring_
        rings.append(ring_)

def generate_nodes(num_nodes):
    if (len(rings) == 1):
        list_id = random.sample(range(0, rings[0].ringsize), num_nodes)
        print list_id
        for i in list_id:
            new_node = node.Node(rings[0].id,i)
            nodes.append(new_node)
            rings[0].nodes.append(new_node)
    else:
        raise NotImplementedError

# def generate_sensors(num_sensors):
#     for
#     list_ss = random.sample(range(0, rings[0].ringsize), num_nodes)

def print_():
    print 'Generate rings list:',
    for element in rings:
        print element.id
    for r in rings:
        r.print_()
def main(argv):
    num_rings = int(argv[0])
    num_nodes = int(argv[1])
    print 'Number of rings:', num_rings
    print 'Number of nodes:', num_nodes
    generate_rings(num_rings)
    generate_nodes(num_nodes)
    print_()
    rings[0].create_()
    # nodes[10].print_()
    # nn = nodes[10]
    # nn.id = 300
    # nodes[10].print_()
    


if __name__ == "__main__":
   main(sys.argv[1:])

