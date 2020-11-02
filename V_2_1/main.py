#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 10:54:10 2020

@author: pierrejablonski
"""

"""
This code tries aims at finding the best RDV point for minimum fuel consumed. 

Assumptions
# 1. Fixed fuel consumption
# 2. Time-constrained incorporating Loiter at RDV point
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
formation_flight_params, A1_flight_params, A2_flight_params = pickle.load(f)
f.close()


destination = formation_flight_params[0];
alpha = formation_flight_params[1];
 
aircraft_1 = A1_flight_params[0];
fuel_burn_1 = A1_flight_params[2];
aircraft_2 = A2_flight_params[0];
fuel_burn_2 = A2_flight_params[2];

equipment_1 = "A333"
equipment_2 = "B763"
V1 = 850; #km/h
V2 = 880; #km/h





# Non-linear BOUNDS
# --------------
bounds = [(-81, 0), (20, 60)]





# Global solver (not really efficient)
# --------------

# x = [long_RDV, lat_RDV, t_loiter]
def f_trajet_haversine(x):
    global aircraft_1, aircraft_2, destination, alpha, fuel_burn_1, fuel_burn_2, V1, V2
    l1 = haversine_distance(aircraft_1[0], aircraft_1[1], x[0], x[1]);
    l2 = haversine_distance(aircraft_2[0], aircraft_2[1], x[0], x[1]);
    l_f = haversine_distance(destination[0], destination[1], x[0], x[1]);
    
    fuel_1 = fuel_burn_1 * l1;
    fuel_2 = fuel_burn_2 * l2;
    fuel_formation = (1-alpha) * (fuel_burn_1 + fuel_burn_2) * l_f
    
    t1 = l1 / V1;
    t2 = l2 / V2;
    
    if min(t1,t2) == t1:    
        V_mD = V1;
        fuel_loiter = abs(t2-t1) * V_mD * fuel_burn_1
    else:
        V_mD = V2;
        fuel_loiter = abs(t2-t1) * V_mD * fuel_burn_2
            
    return fuel_1 + fuel_2 + fuel_formation + fuel_loiter;


# Results HAVERSINE
results = dict();
results['shgo'] = optimize.shgo(f_trajet_haversine, bounds)
RDV = results['shgo'].x
fuel_spent = results['shgo'].fun



# Computing total distance travelled by two planes together
d_1 = haversine_distance(aircraft_1[0], aircraft_1[1], RDV[0], RDV[1])
d_2 = haversine_distance(aircraft_2[0], aircraft_2[1], RDV[0], RDV[1])
d_3 = 2 * haversine_distance(destination[0], destination[1], RDV[0], RDV[1])
total_distance_hvs = d_1 + d_2 + d_3;
time_loiter = abs(d_1/V1 - d_2/V2)

print('\n')
print('Total fuel spent: ', round(fuel_spent/100)/10, 't')
print('Loiter time: ', round(time_loiter*100)/100, 'hr', '\n')


# Create a map showing connections for transatlantic flights
# --------------


# Map parameters
region = [-140, 0, 80, 90] # [long_left, lat_bottom, long_right, lat_top]
output_file = './outputs/map_flight_path.jpg'
res_dpi = 600

# Setting the map
plt.figure(num=1, figsize=(12,12)) 
map=Basemap(llcrnrlon=region[0],llcrnrlat=region[1],urcrnrlon=region[2],urcrnrlat=region[3])
map.fillcontinents(color='grey', alpha=0.3, lake_color='grey')

# Plots the position, destination and RDV points
A1 = map.plot(aircraft_1[0], aircraft_1[1], 'b4', markersize=18, label='Aircraft 1')
A2 = map.plot(aircraft_2[0], aircraft_2[1], 'r4', markersize=18, label='Aircraft 2')
D = map.plot(destination[0], destination[1], 'ko', markersize=8, label='Destination')
RDV_line = map.plot(RDV[0], RDV[1], 'kx', markersize=10, label='RDV')

# Draw the boundaries
p1, p2, p_RDV, p_d = (aircraft_1[0],aircraft_1[1]), (aircraft_2[0],aircraft_2[1]), (RDV[0], RDV[1]), (destination[0], destination[1])
#[point_set, y_1, y_2] = compute_boundaries_great_circle(p1, p2, p_d, 30)
#plt.fill_between(point_set, y_1,y_2, color='#163A6B', alpha=0.15, label='Boundaries', linewidth=0)

# Add connections
line_1 = map.drawgreatcircle(aircraft_1[0],aircraft_1[1],RDV[0],RDV[1], linestyle="solid", linewidth=0.6, color='b', label='Joining route A1')
line_2 = map.drawgreatcircle(aircraft_2[0],aircraft_2[1],RDV[0],RDV[1], linestyle="solid", linewidth=0.6, color='r', label='Joining route A2')
line_formation = map.drawgreatcircle(RDV[0],RDV[1],destination[0],destination[1], linestyle="solid", linewidth=1, color='k', label='Formation flight')
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


#f = open('./workspaces/res_V02_1.pckl', 'wb')
#pickle.dump([RDV, fuel_spent, total_distance_hvs], f)
#f.close()



