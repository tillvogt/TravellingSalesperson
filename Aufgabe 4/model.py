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

    trucktype = ["small", "large"]

    problem = pl.LpProblem("VRP", pl.LpMinimize)    #minizing costs, therefore LpMinize

    X = pl.LpVariable.dicts("x", (locations, locations, [t for t in range(n_trucks)], trucktype), cat=pl.LpBinary)   #variable is a 4dimensional array, first 2 dimensions are a matrix for assigning the routes between 2 locations. third dimension expands with the number of trucks, the fourth is for the different types of trucks
    Y = pl.LpVariable.dicts("y", ([t for t in range(n_trucks)], trucktype), cat=pl.LpBinary)   #decision variable if a truck is needed or not. constraints define that a entry can only be 0 if there is no routing for the referenced truck.
    T = pl.LpVariable.dicts("t", locations, lowBound=0)  #variable that holds arrivaltimes in minutes afer start for each location
    Z = pl.LpVariable.dicts("z", locations, lowBound=0)    #variable wich holds the exceeded deliverytimes in minutes

    D = pl.LpVariable.dicts("d", (restaurants, [t for t in range(n_trucks)], trucktype), lowBound=0, cat=pl.LpInteger) #Variable wich splits the demands on different trucks


    #defining the objective function

    problem += pl.lpSum(pl.lpSum(pl.lpSum(X[i][j][k][l] * d[i][j] for i in locations for j in locations) for k in range(n_trucks)) * var_km for l in trucktype) + pl.lpSum(pl.lpSum(pl.lpSum(X[i][j][k][l] * t[i][j] for i in locations for j in locations) for k in range(n_trucks)) * var_min for l in trucktype) + pl.lpSum(Y[k]["small"] * fix_small for k in range(n_trucks)) + pl.lpSum(Y[k]["large"] * fix_large for k in range(n_trucks)) + pl.lpSum(Z[j]*minute_penalty for j in locations)

    #adding constraints

    problem += T[0] == 0

    for l in trucktype:
        for k in range(n_trucks):
            problem += Y[k][l]*len(locations) >= pl.lpSum(X[i][j][k][l] for i in locations for j in locations) #ensures that Y[k] is only zero, when there are no entries in X Matrix for k
            
            capacity = "cap_"+l
            problem += pl.lpSum(D[j][k][l] for j in restaurants) <= eval(capacity)     #constraint for not exceeding capacity

            for j in locations:
                problem += X[j][j][k][l] == 0  #no selflinks

                problem += pl.lpSum(X[0][j][k][l] for j in locations) == Y[k][l] #starting point for every used truck is 0 in locations 

                problem += pl.lpSum(X[i][j][k][l] for i in locations) - pl.lpSum(X[j][i][k][l] for i in locations) == 0 #means that a truck at a specific location also has to leave it again. with this constraint you can be sure that the developed routes are connected

            for j in restaurants:
                problem += pl.lpSum(X[i][j][k][l] for i in locations)*cap_large >= D[j][k][l] #this ensures that there can only be an capacity assignement, if restaurant j is included in truck ks tour

    for j in restaurants:
        #problem += pl.lpSum(X[i][j][k] for i in locations for k in range(n_trucks)) >= 1    #every locations is visited by at least one truck

        problem += Z[j] >= (T[j]-((7-start)*60)) #Z has to be >= 0 to the exceeded minutes for delivery. the lower bound of the variable is 0.

        problem += pl.lpSum(D[j][k][l] for k in range(n_trucks) for l in trucktype) >= dem[j]  #the delivered goods of all trucks must reach the total demands of each restaurant.

        for l in trucktype:
            for k in range(n_trucks):
                for i in locations:
                    problem += T[j] >= (T[i]+t[i][j]) - (10000*(1-X[i][j][k][l]))  #lower boundary for the arrival times for each location. If there is a connection between to locations in a route, the arrivaltime has to be at least the previous time plus the traveltime

    for l in trucktype:
        subtours = []
        for i in locations[2:]:
            subtours += itertools.combinations(locations[1:], i)

        for s in subtours:
            problem += pl.lpSum(X[i][j][k][l] if i !=j else 0 for i, j in itertools.permutations(s,2) for k in range(n_trucks)) <= len(s) - 1



    problem.solve(pl.PULP_CBC_CMD(timeLimit=500))

    for l in trucktype:
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
                    if i != j and pl.value(X[i][j][k][l]) == 1:
                        plt.plot([xcoor[i], xcoor[j]], [ycoor[i], ycoor[j]], c=colors[k])

        plt.show()