#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 12:27:10 2020

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
from mpl_toolkits.basemap import Basemap
import math as m
from scipy import optimize
plt.style.use('default')
import pickle

from plt_func import add_arrow


# Parameters
# --------------
f = open('./params.pckl', 'rb')
alpha, fuel_burn_1, fuel_burn_2, aircraft_1, aircraft_2, destination = pickle.load(f)
f.close()


# Plane BOUNDS
# --------------

def bounds_plane(x1, y1, x2, y2, x_d, y_d):
    # x rectangular bounds
    if x_d <= min(x1, x2): # destination to the left of the two aircrafts
        bounds_hor = (x_d, max(x1, x2));
    elif x_d >= max(x1, x2): # destination to the right of the two aircrafts
        bounds_hor = (min(x1, x2), x_d);
    elif (x_d > min(x1, x2)) & (x_d < max(x1, x2)): # destination horizontally between the two aircrafts
        bounds_hor = (min(x1, x2), max(x1, x2));
    else:
        print('Error: x out of range');
        
    # y rectangular bounds
    if y_d <= min(y1, y2): # destination below the two aircrafts
        bounds_ver = (y_d, max(y1, y2));
    elif y_d >= max(y1, y2): # destination above the two aircrafts
        bounds_ver = (min(y1, y2), y_d);
    elif (y_d > min(y1, y2)) & (y_d < max(y1, y2)): # destination vertically between the two aircrafts
        bounds_ver = (min(y1, y2), max(y1, y2));
    else:
        print('Error: y out of range');
    
    return [bounds_hor, bounds_ver];


bounds = bounds_plane(aircraft_1[0], aircraft_1[1], aircraft_2[0], aircraft_2[1], destination[0], destination[1])



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
print('Here are the results PLAN: ', results['shgo'].x)
RDV_plan = results['shgo'].x

print(results['shgo'])


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
plt.fill_between([bounds[0][0],bounds[0][1]], bounds[1][0],bounds[1][1], color='#163A6B', alpha=0.15, label='Boundaries', linewidth=0)

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










