import picos

import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate


#Define a separate value to print nicely our outputs :)
def printValues(valuex, valuey, solution): 
    table_data = []
    for i in range(15):
        table_data.append([valuex.value[i], valuey.value[i]])


    headers = ['Where we \n build (by id)', 'Trucks \n per location']

    print(tabulate(table_data, headers = headers, floatfmt=".0f"))
    print('The optimal value for this centers and amount of trucks is:', solution)

def optimizationOne():
    P = picos.Problem()

    x = picos.BinaryVariable('x', 15)                              # Each variable represents if we build or not on that region
    c = picos.IntegerVariable('c', 15, lower = 0)                  # Amount of trucks we buy for each region

    #Cost per square meter in each of the regions
    costSq = np.array([520, 514, 518, 502, 498, 460, 413, 407, 375, 497, 420, 380, 490, 478, 466]) 

    #Land availability per region
    landAv = np.array([95, 110, 76, 86, 104, 94, 110, 96, 84, 102, 90, 108, 102, 84, 84])
    #We set our objetive function --> We want to minimize it
    P.set_objective('min', ( costSq.T * x * 75 + costSq.T * c * 6 + sum(c)*24000 ))              
 
    #Formar un array con costos distintos para los camiones y mostrar como varian
    np.linspace(1, 10)
    np.arange(1,10,1) 

    #Constrains

    # 1) Special constrains --> We tell the program that if we decide to build a center at location 'i', we must buy at least one truck
    for i in range(15):
        P.add_constraint(c[i] <= 1000*x[i]) 
    
    # 2) Land constrains --> Is the place suitable for building the centre?
    for i in range(15):
        P.add_constraint(c[i]*6 <= landAv[i] - 75)

    # 3) Demand constrains --> Which trucks from each center can satisfy the demand of each
    dailyDemands = np.array([9,4,1,5,3,3,8])
    iterations = 15
    totalCosts = []

    for i in range(iterations):
        newDemand=[]
        for i in range(len(dailyDemands)):
            demand = np.random.poisson(lam = dailyDemands[i])
            newDemand.append(demand)

        P.add_constraint((c[0] + c[1] + c[2] + c[3] + c[4] + c[6] + c[7] + c[8] + c[9] + c[10] + c[11] + c[13] + c[14]) * 2 >= newDemand[0])
        P.add_constraint((c[0] + c[1] + c[2] + c[7] + c[8] + c[9] + c[10]) * 2 >= newDemand[1])
        P.add_constraint((c[2] + c[7] + c[8] + c[9] + c[10] + c[11] + c[12]+ c[13]) * 2 >= newDemand[2])
        P.add_constraint((c[1] + c[2] + c[3] + c[4] + c[5] + c[6] + c[7] + c[8] + c[9] + c[10] + c[11] + c[12] + c[13] + c[14]) * 2 >= newDemand[3])
        P.add_constraint((c[1] + c[2] + c[3] + c[4] + c[5] + c[6] + c[7] + c[10] + c[13] + c[14]) * 2 >= newDemand[4])
        P.add_constraint((c[1] + c[2] + c[8] + c[9] + c[10]) * 2 >= newDemand[5])
        P.add_constraint((c[2] + c[4] + c[5] + c[6] + c[7] + c[10] + c[11] + c[12] + c[13] + c[14]) * 2 >= newDemand[6])

        #Es necesario?
        # P.add_constraint(sum(c)*2 >= sum(dailyDemands))

        P.solve()

        totalCosts.append(int(P.value))
        # printValues(x,c,P.value)

    print(totalCosts)

    # Struggling to represent the data
    # # Get the unique values and their counts
    # unique_values, counts = np.unique(totalCosts, return_counts = True)
    # print(unique_values)
    # print(counts)

    # plt.hist(unique_values.tolist(), bins = len(unique_values))
    # plt.xlabel('Total Costs (usd)')
    # plt.ylabel('Frequency')
    # plt.title('Frequency of each total cost')

    # plt.show()

def main():
    optimizationOne()
main()
