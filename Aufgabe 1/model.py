import pulp as pl
import numpy as np
import matplotlib.pyplot as plt
import itertools


def cheese_delivery(
    restaurants,
    locations,
    n_trucks,
    cap,
    cap_small,
    cap_large,
    fix,
    fix_small,
    fix_large,
    var_min,
    var_km,
    unit_penalty,
    minute_penalty,
    start,
    xcoor,
    ycoor,
    t,
    d,
    dem,
    exercise,
):
    #defining model

    problem = pl.LpProblem("VRP", pl.LpMinimize)    #minizing costs, therefore LpMinize

    X = pl.LpVariable.dicts("x", (locations, locations, [t for t in range(n_trucks)]), cat=pl.LpBinary)   #variable is a 3dimensional array, first 2 dimensions are a matrix for assigning the routes between 2 locations. third dimension expands with the number of trucks
    Y = pl.LpVariable.dicts("y", ([t for t in range(n_trucks)]), cat=pl.LpBinary)   #decision variable if a truck is needed or not. constraints define that a entry can only be 0 if there is no routing for the referenced truck.
    T = pl.LpVariable.dicts("t", locations, lowBound=0)  #variable that holds arrivaltimes in minutes afer start for each location
    Z = pl.LpVariable.dicts("z", locations, cat=pl.LpBinary)    #variable wich should assign a 1 if the delivery is too late


    #defining the objective function

    problem += pl.lpSum(pl.lpSum(X[i][j][k] * d[i][j] for i in locations for j in locations) for k in range(n_trucks)) * var_km + pl.lpSum(pl.lpSum(X[i][j][k] * t[i][j] for i in locations for j in locations) for k in range(n_trucks)) * var_min + pl.lpSum(Y[k] * fix for k in range(n_trucks)) + pl.lpSum(Z[j]*unit_penalty for j in locations)

    #adding constraints

    problem += T[0] == 0

    for k in range(n_trucks):
        problem += Y[k]*len(locations) >= pl.lpSum(X[i][j][k] for i in locations for j in locations) #ensures that Y[k] is only zero, when there are no entries in X Matrix for k
        
        problem += pl.lpSum(X[i][j][k] * dem[j] for i in locations for j in restaurants) <= cap   #constraint for not exceeding capacity

        for j in locations:
            problem += X[j][j][k] == 0  #no selflinks

            problem += pl.lpSum(X[0][j][k] for j in locations) == Y[k] #starting point for every used truck is 0 in locations 

            problem += pl.lpSum(X[i][j][k] for i in locations) - pl.lpSum(X[j][i][k] for i in locations) == 0 #means that a truck at a specific location also has to leave it again. with this constraint you can be sure that the developed routes are connected

    for j in restaurants:
        problem += pl.lpSum(X[i][j][k] for i in locations for k in range(n_trucks)) == 1    #every locations is visited only once by one single truck

        problem += Z[j] * 1000 >= (T[j]-((7-start)*60)) #Z has to be 1 if the arrivaltime exceeds 7 o clock

        for k in range(n_trucks):
            for i in locations:

                problem += T[j] >= (T[i]+t[i][j]) - (10000*(1-X[i][j][k]))  #lower boundary for the arrival times for each location. If there is a connection between to locations in a route, the arrivaltime has to be at least the previous time plus the traveltime

    subtours = []
    for i in locations[2:]:
         subtours += itertools.combinations(locations[1:], i)

    for s in subtours:
        problem += pl.lpSum(X[i][j][k] if i !=j else 0 for i, j in itertools.permutations(s,2) for k in range(n_trucks)) <= len(s) - 1



    problem.solve()


    for j in locations:
        print(f"T[{j}] = {T[j].varValue}")



    plt.figure(figsize=(8,8))
    for i in locations:    
        if i == 0:
            plt.scatter(xcoor[i], ycoor[i], c='green', s=200)
            plt.text(xcoor[i], ycoor[i], "depot", fontsize=12)
        else:
            plt.scatter(xcoor[i], ycoor[i], c='orange', s=200)
            plt.text(xcoor[i], ycoor[i], str(locations[i]), fontsize=12)

    colors = ["red", "green", "blue", "yellow", "black", "gray"]

    for k in range(n_trucks):
        for i in locations:
            for j in locations:
                if i != j and pl.value(X[i][j][k]) == 1:
                    plt.plot([xcoor[i], xcoor[j]], [ycoor[i], ycoor[j]], c=colors[k])

    plt.show()