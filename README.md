# Vehicle Routing Optimization

## Overview
This project tackles a variation of the Vehicle Routing Problem (VRP), specifically optimizing cheese delivery routes for multiple vehicles. The goal is to minimize transportation costs while satisfying various constraints such as vehicle capacity, delivery time windows, and customer demands.

## Problem Description
The optimization problem involves:
- Multiple delivery vehicles
- A central depot (KäMaPi)
- Multiple customer locations (restaurants)
- Capacity constraints for vehicles
- Time windows for deliveries
- Penalties for late deliveries

The objective is to find the most cost-effective routes for all vehicles, ensuring that:
1. All customer demands are met
2. Vehicle capacities are not exceeded
3. Delivery time constraints are satisfied (or minimally violated)

## Features
The project implements several variations of the problem, each adding complexity:

1. **Basic VRP with Time Windows**: 
   - Single vehicle type
   - Unit penalty for late deliveries
   - Each restaurant served by one vehicle

2. **VRP with Minute-Based Penalties**:
   - Penalties calculated based on minutes late

3. **Multi-Vehicle Delivery**:
   - Allows multiple vehicles to serve a single restaurant
   - Introduces demand splitting among vehicles

4. **Heterogeneous Fleet**:
   - Two types of vehicles (small and large)
   - Different capacities and operational costs

## Methodology
The problem is modeled using Linear Programming techniques. Key components include:

- **Decision Variables**: 
  - X[i,j,k]: Binary variable for route selection
  - Y[k]: Binary variable for vehicle usage
  - T[j]: Arrival time at each location
  - Z[j]: Penalty variable for late deliveries
  - D[j,k]: Demand fulfilled by each vehicle at each location

- **Objective Function**: 
  Minimizes total cost, including:
  - Distance-based costs
  - Time-based costs
  - Fixed costs per vehicle
  - Penalties for late deliveries

- **Constraints**:
  - Flow conservation
  - Capacity constraints
  - Time window constraints
  - Subtour elimination

## Results
The project successfully solves the VRP for the city of Bern, with visualizations of the optimized routes provided for different problem variations.

![Optimized Routes for Bern](Aufgabe%203/Aufgabe3.png)

The image above shows the optimized delivery routes for the city of Bern under the conditions of the third task, which allows multiple vehicles to serve a single restaurant.

## Technologies Used
- Python (assumed, based on the problem description)
- Linear Programming solver (specific solver not mentioned in the report)

## License
use it, if you need it...
