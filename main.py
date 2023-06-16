import picos

import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate


def optimizationOne():
    P = picos.Problem()

    x = picos.BinaryVariable('x', 15)                   # Each variable represents if we build or not on that region
    c = picos.IntegerVariable('c', 15)                  # Amount of trucks we buy for each region

    #Cost per square meter in each of the regions
    costSq = np.array([520, 514, 518, 502, 498, 460, 413, 407, 375, 497, 420, 380, 490, 478, 466]) 

    #Land availability per region
    landAv = np.array([95, 110, 76, 86, 104, 94, 110, 96, 84, 102, 90, 108, 102, 84, 84])

    #We set our objetive function --> We want to minimize it
    P.set_objective('min', ( costSq.T * x * 75 + costSq.T * c * 6 + sum(c)*24000 ))              

    #Constrains
    #Demand constrains --> Which trucks from each center can satisfy the demand of each
    dailyDemands = np.array([9,4,1,5,3,3,8])

    P.add_constraint((c[0] + c[1] + c[2] + c[3] + c[4] + c[6] + c[7] + c[8] + c[9] + c[10] + c[11] + c[13] + c[14]) * 2 >= dailyDemands[0])
    P.add_constraint((c[0] + c[1] + c[2] + c[7] + c[8] + c[9] + c[10]) * 2 >= dailyDemands[1])
    P.add_constraint((c[2] + c[7] + c[8] + c[9] + c[10] + c[11] + c[12]+ c[13]) * 2 >= dailyDemands[2])
    P.add_constraint((c[1] + c[2] + c[3] + c[4] + c[5] + c[6] + c[7] + c[8] + c[9] + c[10] + c[11] + c[12] + c[13] + c[14]) * 2 >= dailyDemands[3])
    P.add_constraint((c[1] + c[2] + c[3] + c[4] + c[5] + c[6] + c[7] + c[10] + c[13] + c[14]) * 2 >= dailyDemands[4])
    P.add_constraint((c[1] + c[2] + c[8] + c[9] + c[10]) * 2 >= dailyDemands[5])
    P.add_constraint((c[2] + c[4] + c[5] + c[6] + c[7] + c[10] + c[11] + c[12] + c[13] + c[14]) * 2 >= dailyDemands[6])

    #Land constrains --> Is the place suitable for building the centre?
    for i in range(15):
        P.add_constraint(c[i]*6 <= landAv[i] - 75)

    #Trucks constrains
#Constrains
    #Special constrains --> We tell the program that if we decide to build a center at location 'i', we must buy at least one truck
    for i in range(15):
        P.add_constraint(x[i] <= 1000*c[i])
#Probando
    print(P)
    # P.solve()

def main():
    optimizationOne()
main()
