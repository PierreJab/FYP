#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 22:31:53 2020

@author: pierrejablonski
"""

"""
This code tries aims at finding the best RDV point for minimum fuel consumed. 

Assumptions
# 1. Fixed fuel consumption
# 2. Not time-constrained
# 3. Plane space problem
"""


# Libraires
# --------------
import matplotlib.pyplot as plt
from scipy import optimize
import math as m
from mpl_toolkits.basemap import Basemap
import pickle
from plt_func import add_arrow, compute_linear_boundaries



# Parameters
# --------------
f = open('./params.pckl', 'rb')
alpha, fuel_burn_1, fuel_burn_2, aircraft_1, aircraft_2, destination = pickle.load(f)
f.close()


# Linear BOUNDS
# --------------

bounds = [(-81, 0), (20, 60)]



# Global solver (not really efficient)
# --------------

def f_trajet_plan(x):
    global aircraft_1, aircraft_2, destination, alpha, fuel_burn_1, fuel_burn_2
    res_1 = fuel_burn_1 * m.sqrt((x[0] - aircraft_1[0])**2 + (x[1] - aircraft_1[1])**2)
    res_2 = fuel_burn_2 * m.sqrt((x[0] - aircraft_2[0])**2 + (x[1] - aircraft_2[1])**2)
    res_3 = (1-alpha) * m.sqrt((x[0] - destination[0])**2 + (x[1] - destination[1])**2) * (fuel_burn_1 + fuel_burn_2)
    return res_1 + res_2 + res_3;


# Results PLAN
results = dict()
results['shgo'] = optimize.shgo(f_trajet_plan, bounds)
results['DA'] = optimize.dual_annealing(f_trajet_plan, bounds)
results['DE'] = optimize.differential_evolution(f_trajet_plan, bounds)
results['BH'] = optimize.basinhopping(f_trajet_plan, bounds)
print('\nHere are the results PLAN: ', results['shgo'].x, '\n')
RDV_plan = results['shgo'].x







# Create a map showing connections for transatlantic flights
# --------------


# Transatlantic map
region = [-140, 0, 80, 90] # [long_left, lat_bottom, long_right, lat_top]
output_file = './outputs/basemap_flight_path.jpg'
res_dpi = 600

    
# Setting the map
plt.figure(num=1, figsize=(12,12)) 
map=Basemap(llcrnrlon=region[0],llcrnrlat=region[1],urcrnrlon=region[2],urcrnrlat=region[3])
map.fillcontinents(color='grey', alpha=0.3, lake_color='grey')

# Plots the position, destination and RDV points
A1 = map.plot(aircraft_1[0], aircraft_1[1], 'b4', markersize=18, label='Aircraft 1')
A2 = map.plot(aircraft_2[0], aircraft_2[1], 'r4', markersize=18, label='Aircraft 2')
D = map.plot(destination[0], destination[1], 'ko', markersize=8, label='Destination')
RDV = map.plot(RDV_plan[0], RDV_plan[1], 'kx', markersize=10, label='RDV')

# Draw the boundaries
p1, p2, p_RDV, p_d = (aircraft_1[0],aircraft_1[1]), (aircraft_2[0],aircraft_2[1]), (RDV_plan[0], RDV_plan[1]), (destination[0], destination[1])
[x, y1, y2] = compute_linear_boundaries(p1, p2, p_d, 30)
plt.fill_between(x, y1, y2, where=y1>y2, color='#163A6B', alpha=0.15, label='Boundaries', linewidth=0)
           
# Add connections
line_1 = plt.plot([aircraft_1[0],RDV_plan[0]], [aircraft_1[1],RDV_plan[1]], linestyle="solid", linewidth=0.6, color='b', label='Joining route A1')
line_2 = plt.plot([aircraft_2[0],RDV_plan[0]], [aircraft_2[1],RDV_plan[1]], linestyle="solid", linewidth=0.6, color='r', label='Joining route A2')
line_formation = plt.plot([RDV_plan[0], destination[0]], [RDV_plan[1], destination[1]], linestyle="solid", linewidth=1, color='k', label='Formation flight')
plt.plot([aircraft_1[0], destination[0]], [aircraft_1[1], destination[1]], linestyle="dashdot", linewidth=0.6, color='b', label='Alone flight A1')
plt.plot([aircraft_2[0], destination[0]], [aircraft_2[1], destination[1]], linestyle="dashdot", linewidth=0.6, color='r', label='Alone flight A2')

# Add arrows
add_arrow(line_1[0])
add_arrow(line_2[0])
add_arrow(line_formation[0])

# Legend
plt.legend(frameon = True, loc='upper right', edgecolor='1', ncol = 2, borderpad = 1, markerscale = 1.2, labelspacing = 2)

# Saving the file and parameters
plt.gca().set_axis_off()
plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
            hspace = 0, wspace = 0)
plt.margins(0,0)
plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.gca().yaxis.set_major_locator(plt.NullLocator())
plt.savefig(output_file, dpi=res_dpi, bbox_inches = 'tight',
    pad_inches = 0, facecolor='w', edgecolor='w', transparent=True, optimize = True, quality=95)









