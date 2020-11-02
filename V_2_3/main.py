#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 14:17:36 2020

@author: pierrejablonski
"""

"""
This code tries aims at finding the best RDV point for minimum fuel consumed. 

Assumptions
# 1. Fuel fractions:  discretized fuel consumption
# 2. Time-constrained incorporating Loiter at RDV point
# 3. 3D space problem
# 4. BYE incorporated
"""

        
# Libraires
# --------------
import matplotlib.pyplot as plt
from scipy import optimize
import pickle

from maths_func import Timer
from plt_func import surf_J, plot_basemap_results
from flight_class import flight
from class_formation import formation



# Parameters
# --------------
f = open('./params.pckl', 'rb')
formation_flight_params, A1_flight_params, A2_flight_params = pickle.load(f)
f.close()

alpha = formation_flight_params[0];

# Create objects A1 & A2, run preliminary methods
# --------------

A1 = flight(equipment=A1_flight_params[2], orig=A1_flight_params[0], dest=A1_flight_params[1], W_payload=A1_flight_params[3])
A2 = flight(equipment=A2_flight_params[2], orig=A2_flight_params[0], dest=A2_flight_params[1], W_payload=A1_flight_params[3])

for Airc in [A1, A2]:
    Airc.aircraft.populate();
    Airc.aircraft.compute_other_aero_quantities();
    Airc.formation_2.compute_W_ff_end(Airc);


# Run full script for no formation
# --------------

for Airc in [A1, A2]:
    Airc.alone.compute_W_ff_end(Airc);      # Get end of flight fuel fractions
    Airc.alone.compute_W_ff_cruise(Airc);   # Get cruise fuel fractions
    Airc.alone.solve_weights(Airc)          # Solve weights
    Airc.alone.stats(Airc)                  # Get data on the flight



# Non-linear BOUNDS
# --------------

left_bound = min(A1.orig[0], A2.orig[0], A1.dest[0], A2.dest[0])
right_bound = max(A1.orig[0], A2.orig[0], A1.dest[0], A2.dest[0])
bounds = [(left_bound, right_bound), (20, 60), (left_bound, right_bound), (20, 60)]



# Global solver (not really efficient)
# --------------

# x = [long_RDV, lat_RDV, long_BYE, lat_BYE]
def J_min_fuel(x):
    global A1, A2, alpha
                
    # Compute cruise fuel fraction
    A1.formation_2.compute_W_ff_cruise(A1, vector=x, A_other=A2, alph=alpha);
    A2.formation_2.compute_W_ff_cruise(A2, vector=x, A_other=A1, alph=alpha);
    
    # Solve weights
    A1.formation_2.solve_weights(A1)
    A2.formation_2.solve_weights(A2)
    
    # Get data on the flight
    A1.formation_2.stats(A1)
    A2.formation_2.stats(A2)
    
    return A1.formation_2.W_fuel_spent_wo_pb + A2.formation_2.W_fuel_spent_wo_pb;



# Run the optimizer (global solver, not very efficient)
# ---------------------------------------------------------------

time_optimizer = Timer('Optimizer');
with time_optimizer:
    results = dict();
#    results['shgo'] = optimize.shgo(J_min_fuel, bounds)
#    results['DA'] = optimize.dual_annealing(J_min_fuel, bounds)
#    results['DE'] = optimize.differential_evolution(J_min_fuel, bounds)
#    results['BH'] = optimize.basinhopping(J_min_fuel, bounds)
    results['shgo_sobol'] = optimize.shgo(J_min_fuel, bounds, n=200, iters=5,sampling_method='sobol')
    RDV = results['shgo_sobol'].x[0:2]
    BYE = results['shgo_sobol'].x[2:]
    fuel_spent = results['shgo_sobol'].fun


# formation & stats object
# ---------------------------------------------------------------

F = formation(A1, A2, alpha, 2)
print(F.stats.time(A1, A2))
print(F)

# Show results 
# ---------------------------------------------------------------
#print(A1)
#print(A2)
print('\n')
print('-'*20, 'Results', '-'*20)
print('RDV: ', RDV)
print('BYE: ', BYE)
print('Fuel spent alone: ', round((A1.alone.W_fuel_spent_wo_pb + A2.alone.W_fuel_spent_wo_pb)/100)/10, 't')
print('Fuel spent formation: ', round((A1.formation_2.W_fuel_spent_wo_pb + A2.formation_2.W_fuel_spent_wo_pb)/100)/10, 't')
print('Loiter time: ', round(A1.formation_2.loiter_time + A2.formation_2.loiter_time,2), 'hr')
time_optimizer.elapsed(show=True);
print('\n')


# Comparison of solvers 
# ---------------------------------------------------------------






# Surface Plot
# ---------------------------------------------------------------

# Define range
#x = np.arange(bounds[0][0], bounds[0][1])
#y = np.arange(bounds[1][0], bounds[1][1])
#
## Grid points
#xgrid, ygrid = np.meshgrid(x, y)
#xy = np.stack([xgrid, ygrid])
#
## Constructing the J_mat for the plot, Z-coordinates
#J_mat = [];
#for i in range(len(xy[0])):
#    line = [];
#    for j in range(len(xy[0][0])):
#        x_input = [xy[0][i][j], xy[1][i][j]]
#        value = J_min_fuel(x_input);
#        line.append(value);
#    J_mat.append(line);
#J_mat = np.array(J_mat);
#
## Define minimum and output file
#min_P = [RDV[0], RDV[1], fuel_spent/1000]
#output_file_surf = './outputs/surf_J.jpg';

# Run the surf plot function
#surf_J(show=False, X_in = xgrid, Y_in = ygrid, Z_in = J_mat/1000, min_P_in = min_P, view=[5, -165], out_file = output_file_surf)





# Basemap showing formation RDV & BYE
# ---------------------------------------------------------------

# Map parameters
output_file = './outputs/map_flight_path.jpg'
region = [-140, 0, 80, 90] # [long_left, lat_bottom, long_right, lat_top]

plot_basemap_results(show=True, rdv=RDV, bye=BYE, A1_orig=A1.orig, A1_dest=A1.dest, A2_orig=A2.orig, A2_dest=A2.dest, Bounds=bounds, out_file=output_file, Region=region)





# Export key results for comparison
# ---------------------------------------------------------------

#f = open('./workspaces/res_V02_2.pckl', 'wb')
#pickle.dump([RDV, fuel_spent, total_distance_hvs], f)
#f.close()



