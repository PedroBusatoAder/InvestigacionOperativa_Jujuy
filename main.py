import picos

import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate


#Define a separate function to print nicely our outputs :)
def printValues(valueBuild, valueTrucks, valueMotos, solution): 
    table_data = []
    for i in range(15):
        if len(valueMotos) > 0:
            table_data.append([valueBuild.value[i], valueTrucks.value[i], valueMotos.value[i]])
        else:
            table_data.append([valueBuild.value[i], valueTrucks.value[i]])

    headers = ['Where we \n build (by id)', 'Trucks \n per location', 'Motorcycles \n per location']
    print(tabulate(table_data, headers = headers, floatfmt=".0f"))
    print('The optimal value for this centers and amount of trucks is:', solution)

def optimizationOriginal():                                        # Original problem with variable demand
    P = picos.Problem()

    x = picos.BinaryVariable('x', 15)                              # Each variable represents if we build or not on that region
    c = picos.IntegerVariable('c', 15, lower = 0)                  # Amount of trucks we buy for each region --> Each with a price of $24.000

    #Cost per square meter in each of the regions
    costSq = np.array([520, 514, 518, 502, 498, 460, 413, 407, 375, 497, 420, 380, 490, 478, 466]) 

    #Land availability per region
    landAv = np.array([95, 110, 76, 86, 104, 94, 110, 96, 84, 102, 90, 108, 102, 84, 84])

    #We set our objetive function --> We want to minimize it
    P.set_objective('min', ( costSq.T * x * 75 + costSq.T * c * 6 + sum(c)*24000 ))              

    #Constrains
    iterations = 15
    totalCosts = []
    dailyDemand = np.array([9,4,1,5,3,3,8])

    for i in range(iterations):
        # 1) Special constrains --> We tell the program that if we decide to build a center at location 'i', we must buy at least one truck
        for i in range(15):
            P.add_constraint(c[i] <= 1000*x[i])
            
        
        # 2) Land constrains --> Is the place suitable for building the centre?
        for i in range(15):
            P.add_constraint(c[i]*6 <= landAv[i] - 75)

        # 3) Demand constrains --> Which trucks from each center can satisfy the demand of each
        newDemand=[]
        for i in range(len(dailyDemand)):
            demand = np.random.poisson(lam = dailyDemand[i])
            newDemand.append(demand)

        P.add_constraint((c[0] + c[1] + c[2] + c[3] + c[4] + c[6] + c[7] + c[8] + c[9] + c[10] + c[11] + c[13] + c[14]) * 2 >= newDemand[0])
        P.add_constraint((c[0] + c[1] + c[2] + c[7] + c[8] + c[9] + c[10]) * 2 >= newDemand[1])
        P.add_constraint((c[2] + c[7] + c[8] + c[9] + c[10] + c[11] + c[12]+ c[13]) * 2 >= newDemand[2])
        P.add_constraint((c[1] + c[2] + c[3] + c[4] + c[5] + c[6] + c[7] + c[8] + c[9] + c[10] + c[11] + c[12] + c[13] + c[14]) * 2 >= newDemand[3])
        P.add_constraint((c[1] + c[2] + c[3] + c[4] + c[5] + c[6] + c[7] + c[10] + c[13] + c[14]) * 2 >= newDemand[4])
        P.add_constraint((c[1] + c[2] + c[8] + c[9] + c[10]) * 2 >= newDemand[5])
        P.add_constraint((c[2] + c[4] + c[5] + c[6] + c[7] + c[10] + c[11] + c[12] + c[13] + c[14]) * 2 >= newDemand[6])

        P.solve()

        totalCosts.append(int(P.value))
        # printValues(x,c,[],P.value)

        P.remove_all_constraints()                                      #Every time we solve our problem we restart our constraints to avoid them accumulating!

    print(totalCosts)

    unique_values, counts = np.unique(totalCosts, return_counts = True)

    plt.bar(range(len(unique_values)), counts)
    plt.xticks(range(len(unique_values)), unique_values, rotation = 'vertical')

    plt.xlabel('Total Costs (USD)')
    plt.ylabel('Frequency')
    plt.title('Frequency of Each Total Cost')
    plt.show()

def optimizationMotos():                                           # Problem with static demand and motorcycles
    P = picos.Problem()

    x = picos.BinaryVariable('x', 15)                              # Each variable represents if we build or not on that region
    c = picos.IntegerVariable('c', 15, lower = 0)                  # Amount of trucks we buy for each region --> Each with a price of $24.000
    m = picos.IntegerVariable('m', 15, lower = 0)                  # Amount of motorcycles we buy for each region --> Each with a price of $15.000

    #Cost per square meter in each of the regions
    costSq = np.array([520, 514, 518, 502, 498, 460, 413, 407, 375, 497, 420, 380, 490, 478, 466]) 

    #Land availability per region
    landAv = np.array([95, 110, 76, 86, 104, 94, 110, 96, 84, 102, 90, 108, 102, 84, 84])

    #We set our objetive function --> We want to minimize it
    P.set_objective('min', ( costSq.T * x * 75 + costSq.T * c * 6 + costSq.T * m * 2 + sum(c)*24000 + sum(m)*15000 ))              

    #Constrains
    # 1) Special constrains --> We tell the program that if we decide to build a center at location 'i', we must buy at least one truck
    for i in range(15):
        P.add_constraint(c[i] <= 1000*x[i])
        P.add_constraint(m[i] <= 1000*x[i])
         
    # 2) Land constrains --> Is the place suitable for building the centre?
    for i in range(15):
        P.add_constraint(c[i]*6 + m[i]*2 <= landAv[i] - 75)

    # 3) Demand constrains --> Which trucks from each center can satisfy the demand of each
    dailyDemand = np.array([9,4,1,5,3,3,8])

    P.add_constraint((c[0] + c[1] + c[2] + c[3] + c[4] + c[6] + c[7] + c[8] + c[9] + c[10] + c[11] + c[13] + c[14]) * 2 + m[0] + m[1] +m[2] + m[3] + m[4] + m[6] + m[7] + m[8] + m[9] + m[10] + m[11] + m[13] + m[14] >= dailyDemand[0])
    P.add_constraint((c[0] + c[1] + c[2] + c[7] + c[8] + c[9] + c[10]) * 2 + m[0] + m[1] + m[2] + m[7] + m[8] + m[9] + m[10] >= dailyDemand[1])
    P.add_constraint((c[2] + c[7] + c[8] + c[9] + c[10] + c[11] + c[12]+ c[13]) * 2 + m[2] + m[7] + m[8] + m[9] + m[10] + m[11] + m[12]+ m[13] >= dailyDemand[2])
    P.add_constraint((c[1] + c[2] + c[3] + c[4] + c[5] + c[6] + c[7] + c[8] + c[9] + c[10] + c[11] + c[12] + c[13] + c[14]) * 2 + m[1] + m[2] + m[3] + m[4] + m[5] + m[6] + m[7] + m[8] + m[9] + m[10] + m[11] + m[12] + m[13] + m[14] >= dailyDemand[3])
    P.add_constraint((c[1] + c[2] + c[3] + c[4] + c[5] + c[6] + c[7] + c[10] + c[13] + c[14]) * 2 + m[1] + m[2] + m[3] + m[4] + m[5] + m[6] + m[7] + m[10] + m[13] + m[14] >= dailyDemand[4])
    P.add_constraint((c[1] + c[2] + c[8] + c[9] + c[10]) * 2 + m[1] + m[2] + m[8] + m[9] + m[10] >= dailyDemand[5])
    P.add_constraint((c[2] + c[4] + c[5] + c[6] + c[7] + c[10] + c[11] + c[12] + c[13] + c[14]) * 2 + m[2] + m[4] + m[5] + m[6] + m[7] + m[10] + m[11] + m[12] + m[13] + m[14] >= dailyDemand[6])

    P.solve()

    printValues(x,c,m,P.value)
    
def optimizationCapacities():                                      # Sensibility analysis with variable demand capacities for trucks and motorcycles

    P = picos.Problem()

    x = picos.BinaryVariable('x', 15)                              # Each variable represents if we build or not on that region
    c = picos.IntegerVariable('c', 15, lower = 0)                  # Amount of trucks we buy for each region --> Each with a price of $24.000
    m = picos.IntegerVariable('m', 15, lower = 0)                  # Amount of motorcycles we buy for each region --> Each with a price of $10.000

    #Cost per square meter in each of the regions
    costSq = np.array([520, 514, 518, 502, 498, 460, 413, 407, 375, 497, 420, 380, 490, 478, 466]) 

    #Land availability per region
    landAv = np.array([95, 110, 76, 86, 104, 94, 110, 96, 84, 102, 90, 108, 102, 84, 84])

    #We set our objetive function --> We want to minimize it
    P.set_objective('min', ( costSq.T * x * 75 + costSq.T * c * 6 + costSq.T * m * 2 + sum(c)*24000 + sum(m)*15000 ))              

    #Constrains
    results = []                                    # Array which will contain the results for all the different combinations of capacities for our transports --> Each element of the array will be an array in itself with three elements
    dailyDemand = np.array([9,4,1,5,3,3,8])
    truckCapacities = [1,2,3,4]
    motorcycleCapacities = [1,2,3,4]

    for k in range(len(truckCapacities)): 

        # 1) Special constrains --> We tell the program that if we decide to build a center at location 'i', we must buy at least one truck
        for i in range(15):
            P.add_constraint(c[i] <= 1000*x[i])
            P.add_constraint(m[i] <= 1000*x[i])
                
        # 2) Land constrains --> Is the place suitable for building the centre?
        for i in range(15):
            P.add_constraint(c[i]*6 + m[i]*2 <= landAv[i] - 75)

        # 3) Demand constrains --> Which trucks from each center can satisfy the demand of each
        for j in range(len(motorcycleCapacities)):
            P.add_constraint( (c[0] + c[1] + c[2] + c[3] + c[4] + c[6] + c[7] + c[8] + c[9] + c[10] + c[11] + c[13] + c[14]) * truckCapacities[k] + (m[0] + m[1] +m[2] + m[3] + m[4] + m[6] + m[7] + m[8] + m[9] + m[10] + m[11] + m[13] + m[14]) * motorcycleCapacities[j] >= dailyDemand[0])
            P.add_constraint( (c[0] + c[1] + c[2] + c[7] + c[8] + c[9] + c[10]) * truckCapacities[k] + (m[0] + m[1] + m[2] + m[7] + m[8] + m[9] + m[10]) *  motorcycleCapacities[j] >= dailyDemand[1])
            P.add_constraint( (c[2] + c[7] + c[8] + c[9] + c[10] + c[11] + c[12]+ c[13]) * truckCapacities[k] + (m[2] + m[7] + m[8] + m[9] + m[10] + m[11] + m[12]+ m[13]) * motorcycleCapacities[j] >= dailyDemand[2])
            P.add_constraint( (c[1] + c[2] + c[3] + c[4] + c[5] + c[6] + c[7] + c[8] + c[9] + c[10] + c[11] + c[12] + c[13] + c[14]) * truckCapacities[k] + (m[1] + m[2] + m[3] + m[4] + m[5] + m[6] + m[7] + m[8] + m[9] + m[10] + m[11] + m[12] + m[13] + m[14]) * motorcycleCapacities[j] >= dailyDemand[3])
            P.add_constraint( (c[1] + c[2] + c[3] + c[4] + c[5] + c[6] + c[7] + c[10] + c[13] + c[14]) * truckCapacities[k] + (m[1] + m[2] + m[3] + m[4] + m[5] + m[6] + m[7] + m[10] + m[13] + m[14]) * motorcycleCapacities[j] >= dailyDemand[4])
            P.add_constraint( (c[1] + c[2] + c[8] + c[9] + c[10]) * truckCapacities[k] + (m[1] + m[2] + m[8] + m[9] + m[10]) * motorcycleCapacities[j] >= dailyDemand[5])
            P.add_constraint( (c[2] + c[4] + c[5] + c[6] + c[7] + c[10] + c[11] + c[12] + c[13] + c[14]) * truckCapacities[k] + (m[2] + m[4] + m[5] + m[6] + m[7] + m[10] + m[11] + m[12] + m[13] + m[14]) * motorcycleCapacities[j] >= dailyDemand[6])
            
            P.solve()
            printValues(x,c,m,P.value)
            results.append([sum(c.value), sum(m.value), P.value])
            for i in range(51, 44, -1):
                P.remove_constraint(i)

        P.remove_all_constraints()

    print(results)

def main():
    # optimizationOriginal()
    # optimizationMotos()
    optimizationCapacities()
main()
