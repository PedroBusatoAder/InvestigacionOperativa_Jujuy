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
    #Demand constrains --> How many demands can each truck satisfy
    dailyDemands = np.array([9,4,1,5,3,3,8])
    for i in range(len(dailyDemands)):
        P.add_constraint(c[i] * 2 )

    #Land constrains --> Is the place suitable for building the centre?
    for i in range(15):
        P.add_constraint(x[i]*75 + c[i]*6 <= landAv[i])

    #Trucks constrains
    

    print(P)
    # P.solve()

def main():
    optimizationOne()
main()
