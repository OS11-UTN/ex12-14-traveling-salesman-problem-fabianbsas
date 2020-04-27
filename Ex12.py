#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: fabian
"""

import numpy
from scipy.optimize import linprog
from Utils import transform_NN_to_NA
import matplotlib.pyplot as pyplot
import random 
from scipy.spatial import distance

# create a random list of nodes
def create_nodes(quantity_of_nodes): 
    random.seed(a=33)
    nodes = []
    for idx in range(quantity_of_nodes):
        for jdx in range(2):
            if idx != jdx:
                node = (random.randint(0, 100), random.randint(0, 100)) 
                nodes.append(node)
    return nodes



total_nodes = 50
nodes = create_nodes(total_nodes)

distance_vector = []
for idx in range(total_nodes):
   for jdx in range(total_nodes):
      if idx != jdx:
         distance_vector.append(distance.euclidean(nodes[idx], nodes[jdx])) 
        

# Create a n*n matrix filled with 1 and zeros in the diagonal
matrix_node_node = numpy.ones(shape=(total_nodes, total_nodes))
numpy.fill_diagonal(matrix_node_node, 0)

matrix_node_arch, arc_idxs = transform_NN_to_NA(matrix_node_node)

Aeq1 = numpy.where(matrix_node_arch == 1, 1, 0)
#print(Aeq1)
Aeq2 = numpy.where(matrix_node_arch == -1, 1, 0)
#print(Aeq2)
Aeq = numpy.concatenate((Aeq1, Aeq2), axis=0)
#print(Aeq)

beq = numpy.ones(total_nodes * 2)

bounds = tuple([(0, None) for arc in range(0, Aeq.shape[1])])



#optimization
#result = linprog(distance_vector, A_eq=Aeq, b_eq=beq, bounds=bounds, method='simplex')
result = linprog(distance_vector, A_eq=Aeq, b_eq=beq, bounds=bounds, method='revised simplex')

#printing the solution
Active = []
for idx in range(total_nodes):
    temp = list(result.x[(total_nodes-1)*idx:(total_nodes-1)*(idx+1)])
    temp.insert(idx, 0.0)
    Active.append(temp)


print("\n\n## Results ## \n\n")
print("\tActivated arcs: ")
for i in range(len(result.x)):
    if result.x[i] != 0:
        print("\t\tThis arc {} has a cost {}".format(arc_idxs[i],distance_vector[i]))

print("\n\tTotal Cost:", result.fun)

# plot the solution
for i in range(total_nodes):
    for j in range(total_nodes):
        if Active[i][j] == 1:
            x = [nodes[i][0], nodes[j][0]]
            y = [nodes[i][1], nodes[j][1]]
            pyplot.plot(x, y, 'ro-')
pyplot.show()

"""
This method can find subtours but it doesn't find the optimal path. 

There is different strategies we can use to improve the solution like implement Dantzig's restrictions 
or relaxing some constraints. Other alternative could be use a metaheuristic algorithm like GRASP

For a small number of nodes like 30 or 50 the execution is fast even if it doesn't find an optimal solution, 
but for a large number of nodes (I tried with 1000) after 20 minutes of execution the process doesn't end and 
consume a large amoun of memory.

"""
