#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 23:04:01 2020

@author: pierrejablonski
"""

"""
This code tries aims at finding the best RDV point for minimum fuel consumed. 

Assumptions
# 1. Fixed fuel consumption
# 2. Not time-constrained
# 3. 3D space problem
"""

# https://pypi.org/project/great-circle-calculator/
# https://docs.scipy.org/doc/scipy/reference/tutorial/optimize.html#unconstrained-minimization-of-multivariate-scalar-functions-minimize

# Libraires
# --------------
import matplotlib.pyplot as plt
from scipy import optimize
from mpl_toolkits.basemap import Basemap
import great_circle_calculator.great_circle_calculator as gcc
import pickle

from maths_func import haversine_distance
from plt_func import add_arrow, compute_boundaries_great_circle



# Parameters
# --------------
f = open('./params.pckl', 'rb')
alpha, fuel_burn_1, fuel_burn_2, aircraft_1, aircraft_2, destination = pickle.load(f)
f.close()



# Non-linear BOUNDS
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
bounds = [(-81, 0), (20, 60)]


# Global solver (not really efficient)
# --------------

def f_trajet_haversine(x):
    global aircraft_1, aircraft_2, destination, alpha, fuel_burn_1, fuel_burn_2
    res_1 = fuel_burn_1 * haversine_distance(aircraft_1[0], aircraft_1[1], x[0], x[1])
    res_2 = fuel_burn_2 * haversine_distance(aircraft_2[0], aircraft_2[1], x[0], x[1])
    res_3 = (1-alpha) * (fuel_burn_1 + fuel_burn_2) * haversine_distance(destination[0], destination[1], x[0], x[1])
    return res_1 + res_2 + res_3;


# Results HAVERSINE
results = dict();
results['shgo'] = optimize.shgo(f_trajet_haversine, bounds)
results['DA'] = optimize.dual_annealing(f_trajet_haversine, bounds)
results['DE'] = optimize.differential_evolution(f_trajet_haversine, bounds)
results['BH'] = optimize.basinhopping(f_trajet_haversine, bounds)
RDV_hvs = results['shgo'].x
fuel_spent_hvs = results['shgo'].fun

print('\n', 'Total fuel spent using great circle formation: ', round(results['shgo'].fun/100)/10, 't', '\n')

# Computing total distance travelled by two planes together
d_1 = haversine_distance(aircraft_1[0], aircraft_1[1], RDV_hvs[0], RDV_hvs[1])
d_2 = haversine_distance(aircraft_2[0], aircraft_2[1], RDV_hvs[0], RDV_hvs[1])
d_3 = 2 * haversine_distance(destination[0], destination[1], RDV_hvs[0], RDV_hvs[1])
total_distance_hvs = d_1 + d_2 + d_3;

# Create a map showing connections for transatlantic flights
# --------------


# Map parameters
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
RDV = map.plot(RDV_hvs[0], RDV_hvs[1], 'kx', markersize=10, label='RDV')

# Draw the boundaries
p1, p2, p_RDV, p_d = (aircraft_1[0],aircraft_1[1]), (aircraft_2[0],aircraft_2[1]), (RDV_hvs[0], RDV_hvs[1]), (destination[0], destination[1])
#[point_set, y_1, y_2] = compute_boundaries_great_circle(p1, p2, p_d, 30)
#plt.fill_between(point_set, y_1,y_2, color='#163A6B', alpha=0.15, label='Boundaries', linewidth=0)

# Add connections
line_1 = map.drawgreatcircle(aircraft_1[0],aircraft_1[1],RDV_hvs[0],RDV_hvs[1], linestyle="solid", linewidth=0.6, color='b', label='Joining route A1')
line_2 = map.drawgreatcircle(aircraft_2[0],aircraft_2[1],RDV_hvs[0],RDV_hvs[1], linestyle="solid", linewidth=0.6, color='r', label='Joining route A2')
line_formation = map.drawgreatcircle(RDV_hvs[0],RDV_hvs[1],destination[0],destination[1], linestyle="solid", linewidth=1, color='k', label='Formation flight')
map.drawgreatcircle(aircraft_1[0],aircraft_1[1],destination[0],destination[1], linestyle="dashdot", linewidth=0.6, color='b', label='Alone flight A1')
map.drawgreatcircle(aircraft_2[0],aircraft_2[1],destination[0],destination[1], linestyle="dashdot", linewidth=0.6, color='r', label='Alone flight A2')

# Add arrows
midpoint_flight_1 = gcc.intermediate_point(p1, p_RDV, fraction=0.5)
midpoint_flight_2 = gcc.intermediate_point(p2, p_RDV, fraction=0.5)
midpoint_flight_form = gcc.intermediate_point(p_RDV, p_d, fraction=0.5)
add_arrow(line_1[0], position=midpoint_flight_1)
add_arrow(line_2[0], position=midpoint_flight_2)
add_arrow(line_formation[0], position=midpoint_flight_form)

# Legend
plt.legend(frameon = True, loc='upper right', edgecolor='1', ncol = 2, borderpad = 1, markerscale = 1.2, labelspacing = 2, facecolor='white')

# Saving the file and parameters
plt.gca().set_axis_off()
plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
            hspace = 0, wspace = 0)
plt.margins(0,0)
plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.gca().yaxis.set_major_locator(plt.NullLocator())
plt.savefig(output_file, dpi=res_dpi, bbox_inches = 'tight',
    pad_inches = 0, facecolor='w', edgecolor='w', transparent=True, optimize = True, quality=95)





# SAVING DATA FOR COMPARISON


#f = open('./workspaces/res_V01_3.pckl', 'wb')
#pickle.dump([RDV_hvs, fuel_spent_hvs, total_distance_hvs], f)
#f.close()
