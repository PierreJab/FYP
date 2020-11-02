#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 14:17:36 2020

@author: pierrejablonski
"""

"""
This code tries aims at finding the best RDV point for minimum fuel consumed. 

Assumptions
# 1. Evolutive fuel consumption
# 2. Time-constrained incorporating Loiter at RDV point
# 3. 3D space problem
"""

# https://docs.scipy.org/doc/scipy/reference/tutorial/optimize.html#unconstrained-minimization-of-multivariate-scalar-functions-minimize

# Libraires
# --------------
import matplotlib.pyplot as plt
import numpy as np
#from copy import deepcopy
from mpl_toolkits.mplot3d import Axes3D
from scipy import optimize
from mpl_toolkits.basemap import Basemap
import great_circle_calculator.great_circle_calculator as gcc
import pickle

#from maths_func import haversine_distance
from plt_func import add_arrow, compute_boundaries_great_circle
from flight_class import flight

# Parameters
# --------------
f = open('./params.pckl', 'rb')
formation_flight_params, A1_flight_params, A2_flight_params = pickle.load(f)
f.close()

destination = formation_flight_params[0];
alpha = formation_flight_params[1];
 
aircraft_1 = A1_flight_params[0];
aircraft_2 = A2_flight_params[0];



# Create objects A1 & A2, run preliminary methods
# --------------

A1 = flight(equipment=A1_flight_params[3], orig=A1_flight_params[0], dest=A1_flight_params[1], W_payload=A1_flight_params[4])
A2 = flight(equipment=A2_flight_params[3], orig=A2_flight_params[0], dest=A2_flight_params[1], W_payload=A1_flight_params[4])

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



# Results HAVERSINE
results = dict();
results['shgo'] = optimize.shgo(J_min_fuel, bounds)
results['DA'] = optimize.dual_annealing(J_min_fuel, bounds)
results['DE'] = optimize.differential_evolution(J_min_fuel, bounds)
results['BH'] = optimize.basinhopping(J_min_fuel, bounds)
results['shgo_sobol'] = optimize.shgo(J_min_fuel, bounds, n=200, iters=5,sampling_method='sobol')
RDV = results['shgo_sobol'].x
fuel_spent = results['shgo_sobol'].fun





# Show results 
print(A1)
print(A2)
print('\n')
print('Fuel spent alone: ', round((A1.alone.W_fuel_spent_wo_pb + A2.alone.W_fuel_spent_wo_pb)/100)/10, 't')
print('Fuel spent formation: ', round((A1.formation_2.W_fuel_spent_wo_pb + A2.formation_2.W_fuel_spent_wo_pb)/100)/10, 't')
print('Loiter time: ', round(A1.formation_2.loiter_time + A2.formation_2.loiter_time,2), 'hr', '\n')



# FUNCTION MAP

# ---------------------------------------------------------------
x = np.arange(bounds[0][0], bounds[0][1])
y = np.arange(bounds[1][0], bounds[1][1])

xgrid, ygrid = np.meshgrid(x, y)
xy = np.stack([xgrid, ygrid])

# Constructing the J_mat for the plot, Z-coordinates
J_mat = [];
for i in range(len(xy[0])):
    line = [];
    for j in range(len(xy[0][0])):
        x_input = [xy[0][i][j], xy[1][i][j]]
        value = J_min_fuel(x_input);
        line.append(value);
    J_mat.append(line);

J_mat = np.array(J_mat);
# ---------------------------------------------------------------

# def 3D_min_plot(min_P, xgrid, ygrid, J_mat, output_file, view)
# min_P = [x_min, y_min, z_min] = [RDV[0], RDV[1], fuel_spent/1000]
fig1 = plt.figure(num=1, figsize=(8,6)) 

# Define axis and orientiation
#ax = fig1.add_subplot(111, projection='3d')
ax = fig1.gca(projection='3d')
#ax.view_init(45, -45)
ax.view_init(5, -165)

# Plot
cb = ax.plot_surface(xgrid, ygrid, J_mat/1000, cmap='ocean', zorder=2, alpha=0.6, edgecolors='None', lw=0.0)
ax.scatter(RDV[0], RDV[1], fuel_spent/1000, color='black', linewidth=10, zorder=10, label='Minimum')

# Legend
plt.legend(frameon = True, loc='upper right', edgecolor='1', ncol = 2, borderpad = 1, markerscale = 1.2, labelspacing = 2, facecolor='white')

# set labels
ax.set_xlabel('RDV longitude', fontsize=10, fontweight='black', color = '#333F4B')
ax.set_ylabel('RDV latitude', fontsize=10, fontweight='black', color = '#333F4B')
plt.annotate("Fuel spent (tonnes)",(0.1,0.83), xycoords="figure fraction", fontsize=10, fontweight='black', color = '#333F4B')
    
# Impose the number of ticks on the axis
plt.locator_params(axis='y', nbins=6)
plt.locator_params(axis='x', nbins=4)

# Grid lines
grid_lines = {"linewidth":0, "color" : "w", "linestyle" : "-"}
ax.xaxis._axinfo["grid"].update(grid_lines)
ax.yaxis._axinfo["grid"].update(grid_lines)
ax.zaxis._axinfo["grid"].update({"linewidth":0.2, "color" : "grey", "linestyle" : "-", "alpha":"0.3"})

# Colorbar
fig1.colorbar(cb)    
          
plt.show()
fig1.savefig('./outputs/surf_J.jpg', dpi=900, bbox_inches = 'tight',
    pad_inches = 0, facecolor='w', edgecolor='w', transparent=True, optimize = True, quality=95)












from mpl_toolkits.axes_grid1 import make_axes_locatable


# Set font 
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'FontAwesome'

# set the style of the axes and the text color
plt.rcParams['axes.edgecolor']='#333F4B'
plt.rcParams['axes.linewidth']=0.8
plt.rcParams['xtick.color']='#333F4B'
plt.rcParams['ytick.color']='#333F4B'
plt.rcParams['text.color']='#333F4B'


fig2 = plt.figure(figsize=(8,6))
ax1 = fig2.add_subplot(111)
im = plt.imshow(J_mat, interpolation='bicubic', origin='lower',cmap='Greys', extent =[bounds[0][0], bounds[0][1], bounds[1][0], bounds[1][1]])

# set labels
ax1.set_xlabel('Longitude', fontsize=10, fontweight='black', color = '#333F4B')
ax1.set_ylabel('')
fig2.text(0.1, 0.86, 'Latitude', fontsize=10, fontweight='black', color = '#333F4B')
         
# set axis
ax1.tick_params(axis='both', which='major', labelsize=9)

# change the style of the axis spines
ax1.spines['top'].set_color('none')
ax1.spines['right'].set_color('none')
ax1.spines['left'].set_smart_bounds(True)
ax1.spines['bottom'].set_smart_bounds(True)

plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=True,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=True) # labels along the bottom edge are off



def plot_point(res, marker='o', color=None, label=None):
    ax1.plot(res.x[0], res.x[1], marker=marker, color=color, ms=6, label=label)

plot_point(results['BH'], color='y', label="BH")  # basinhopping           - yellow
plot_point(results['DE'], color='c', label="DE")  # differential_evolution - cyan
plot_point(results['DA'], color='k', label="DA")  # dual_annealing.        - white

# SHGO produces multiple minima, plot them all (with a smaller marker size)
plot_point(results['shgo'], color='k', marker='+', label="shgo")
plot_point(results['shgo_sobol'], color='k', marker='x', label="shgo sobol")
for i in range(results['shgo_sobol'].xl.shape[0]):
    if i == 0:
        ax1.plot(results['shgo_sobol'].xl[i, 0],
            results['shgo_sobol'].xl[i, 1],
            'ko', ms=2, label="shgo sobol \nlocal minimizer")
    else:
        ax1.plot(results['shgo_sobol'].xl[i, 0],
                results['shgo_sobol'].xl[i, 1],
                'ko', ms=2)

ax1.set_xlim([bounds[0][0], bounds[0][1]])
ax1.set_ylim([8, 60])

# COLORBAR SIZE AND LOCATION
#divider = make_axes_locatable(ax1)
#cax = divider.append_axes("right", size="5%", pad=0.5)

# Legend
plt.legend(frameon = True, loc='upper right', edgecolor='1', ncol = 1, borderpad = 1, markerscale = 1, labelspacing = 0.8, facecolor='white', fontsize=9)

#plt.colorbar(cax=cax)
#plt.colorbar(orientation="horizontal")

plt.show()

# Save and export the figure
fig2.savefig('./outputs/minimizers.jpg', dpi=900, bbox_inches = 'tight',
    pad_inches = 0, facecolor='w', edgecolor='w', transparent=True, optimize = True, quality=95)















# Create a map showing connections for transatlantic flights
# --------------

# Map parameters
region = [-140, 0, 80, 90] # [long_left, lat_bottom, long_right, lat_top]
output_file = './outputs/map_flight_path.jpg'
res_dpi = 600

# Setting the map
fig2 = plt.figure(num=2, figsize=(12,12)) 
map=Basemap(llcrnrlon=region[0],llcrnrlat=region[1],urcrnrlon=region[2],urcrnrlat=region[3])
map.fillcontinents(color='grey', alpha=0.3, lake_color='grey')

# Plots the position, destination and RDV points
A1 = map.plot(A1.orig[0], A1.orig[1], 'b4', markersize=18, label='Aircraft 1')
A2 = map.plot(A2.orig[0], A2.orig[1], 'r4', markersize=18, label='Aircraft 2')
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
fig2.savefig(output_file, dpi=res_dpi, bbox_inches = 'tight',
    pad_inches = 0, facecolor='w', edgecolor='w', transparent=True, optimize = True, quality=95)




# SAVING DATA


#f = open('./workspaces/res_V02_2.pckl', 'wb')
#pickle.dump([RDV, fuel_spent, total_distance_hvs], f)
#f.close()



