import os
from subprocess import Popen, PIPE
from pulp import *

"""
setcover problem
"""

def solve_it(input_data):
    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    item_count = int(parts[0])
    set_count = int(parts[1])
    
    sets = range(set_count)
    items = range(item_count)
    setCost = {}
    setItems = []
    setItems_tuple = []
    for i in range(1, set_count+1):
        s = i-1
        parts = lines[i].split()
        setCost[s] = float(parts[0])
        itemsToAdd = map(int, parts[1:])
        setItems.append(itemsToAdd)
        # for i in itemsToAdd:
        #     setItems_tuple.extend([s,i])
    # print setItems
    setItems_tuple = [(i,s) for s in sets for i in setItems[s]]
    # print setItems_tuple
    
    # print setCost
    # print setItems

 # MODEL:

    model= LpProblem("setcover", LpMinimize)

    #we define two variables: 
    # set_chosen: if a set is chosen or not
    # item_chosen_by_set: if an item is chosen or because of a particular set
    # the second makes the model bigger but helps in the relaxation

    set_chosen = LpVariable.dicts("set", sets, 0, 1, LpInteger)
    # item_chosen_by_set = LpVariable.dicts("item_set", setItems_tuple, 0, 1, LpInteger)
    # item_chosen = LpVariable.dicts("item", items, 0, 1, LpInteger)
    # print item_chosen_by_set
    #Objective function
    model += lpSum([set_chosen[i]*setCost[i] for i in sets]), "Total cost of sets"

    #Constraints:

    # option 1: simple model, one variable, one contraint.
    for i in items:
        model += lpSum([set_chosen[s] for s in sets if i in setItems[s]]) >= 1, "at least one set covers item %i" % i
	
    # option 2: three variables, three constraints.
    # for s in sets:
        # for i in setItems[s]:
            # model += item_chosen_by_set[i,s] <= set_chosen[s], "if set %i is not chosen: it cannot cover item %i" % (s, i)
    
    # for s in sets:
        # for i in setItems[s]:
            # model += item_chosen_by_set[i,s] >= item_chosen[i], "if set %i covers item %i: the item is selected" % (s, i)
             
    # for i in items:
        # model += lpSum([item_chosen_by_set[i,s] for s in sets if i in setItems[s]]) >= 1, "at least one set covers item %i" % i
	

    model.writeLP("ejemplo.pl")
    # COIN_CMD, PULP_CBC_CMD, GLPK_CMD
    model.solve(GLPK_CMD())
    # model.solve()

    output_data = str(int(value(model.objective))) + ' ' + str(1) + '\n'

    for s in sets:
    	output_data += str(int(value(set_chosen[s])))+ " "        

    return output_data

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print 'Solving:', file_location
        print solve_it(input_data)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/sc_6_1)'

