#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 23:37:09 2020

@author: pierrejablonski
"""

"""
This file contains plot functions for the purpose of V-Formation Masters Thesis
"""


# Libraires
# --------------
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
from mpl_toolkits.basemap import Basemap
import great_circle_calculator.great_circle_calculator as gcc

from maths_func import points_on_great_circle


def add_arrow(line, position=None, direction='right', size=15, color=None):
    """
    add an arrow to a line.

    line:       Line2D object
    direction:  'left' or 'right'
    size:       size of the arrow in fontsize points
    color:      if None, line color is taken.
    """
    if color is None:
        color = line.get_color()

    xdata = line.get_xdata()
    ydata = line.get_ydata()
    
    if position is None:
        pos_x = xdata.mean();
        pos_y = ydata.mean();
    else:
        pos_x = position[0];
        pos_y = position[1];
        
    gradient = (ydata[0] - ydata[-1])/(xdata[0] - xdata[-1]);
    plt.arrow(pos_x, pos_y, 1, gradient, shape='full', lw=0, length_includes_head=True, head_width=2, color=color)




def compute_linear_boundaries(p1, p2, p_d, n):
    a2 = (p_d[1] - p2[1])/(p_d[0] - p2[0]); # coefficient directeur
    b2 = p_d[1] - a2*p_d[0]
    point_INT = (p1[0], a2*p1[0]+ b2)
    
    a1_bef = (p1[1] - p2[1])/(p1[0] - p2[0]); # coefficient directeur
    a1_aft = (p_d[1] - p1[1])/(p_d[0] - p1[0]); # coefficient directeur
    b1_bef = p1[1] - a1_bef*p1[0]; # y = ax + b
    b1_aft = p1[1] - a1_aft*p1[0];
    
    x_set_bef_INT = np.linspace(p2[0], point_INT[0], n);
    x_set_aft_INT = np.linspace(point_INT[0], p_d[0], n);
    x = np.concatenate((x_set_bef_INT, x_set_aft_INT), axis=0);
    
    y1_bef = a1_bef * x_set_bef_INT + b1_bef;
    y1_aft = a1_aft * x_set_aft_INT + b1_aft;
    y1 = np.concatenate((y1_bef, y1_aft), axis=0);
    y2 = a2 * x + b2;
    
    return [x, y1, y2]



def compute_boundaries_great_circle(p1, p2, p_d, n):
    
    # Discretize the trajectories, interpolate and define 'intermediate' point
    points_1_D = points_on_great_circle(p1, p_d, n)
    points_2_D = points_on_great_circle(p2, p_d, n)
    points_1_2 = points_on_great_circle(p1, p2, n)
    f = interp1d(points_2_D[0], points_2_D[1], kind='cubic')
    p2_int_d = (p1[0], f(p1[0]))
    points_2int_D = points_on_great_circle(p2_int_d, p_d, n)
    points_2_2int = points_on_great_circle(p2, p2_int_d, n)
    
    # Generate discrete points before Intermediate, for flight 1 & 2
    f_interp_2_before_D = interp1d(points_2_2int[0], points_2_2int[1], kind='cubic')
    f_interp_1_before_D = interp1d(points_1_2[0], points_1_2[1], kind='cubic')  
    point_set_before_D = np.linspace(p2[0], p1[0], n);
    y_1_before_D = f_interp_1_before_D(point_set_before_D)
    y_2_before_D = f_interp_2_before_D(point_set_before_D)
    
    # Generate discrete points after Intermediate, for flight 1 & 2
    f_interp_2_after_D = interp1d(points_2int_D[0], points_2int_D[1], kind='cubic')
    f_interp_1_adter_D = interp1d(points_1_D[0], points_1_D[1], kind='cubic')      
    point_set_after_D = np.linspace(p1[0], p_d[0], n);
    y_1_after_D = f_interp_1_adter_D(point_set_after_D)
    y_2_after_D = f_interp_2_after_D(point_set_after_D)
    
    # Concatenate
    point_set = np.concatenate((point_set_before_D, point_set_after_D), axis=0);
    y_1 = np.concatenate((y_1_before_D, y_1_after_D), axis=0)
    y_2 = np.concatenate((y_2_before_D, y_2_after_D), axis=0)
    
    return [point_set, y_1, y_2]




def surf_J(**kwargs):
    
    # Retrieving the arguments
    show = kwargs.get('show', True)
    view = kwargs.get('view', [45, 45]);
    X = kwargs.get('X_in', None);
    Y = kwargs.get('Y_in', None);
    Z = kwargs.get('Z_in', None);
    min_P = kwargs.get('min_P_in', None);
    output_file = kwargs.get('out_file', None);
    [x_min, y_min, z_min] = min_P;

    # Define figure
    fig = plt.figure(num=1, figsize=(8,6)) 
    
    # Define axis and orientiation
    ax = fig.add_subplot(111, projection='3d')
    ax.view_init(view[0], view[1])
    
    # Plot
    cb = ax.plot_surface(X, Y, Z, cmap='ocean', zorder=2, alpha=0.6, edgecolors='None', lw=0.0)
    ax.scatter(x_min, y_min, z_min, color='black', linewidth=10, zorder=10, label='Minimum')
    
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
    fig.colorbar(cb)    
            
    # Show/hide figure
    if not show: 
        plt.close();
    else:
        plt.show();
    
    # Save and export the figure
    fig.savefig(output_file, dpi=900, bbox_inches = 'tight',
        pad_inches = 0, facecolor='w', edgecolor='w', transparent=True, optimize = True, quality=95)







def plot_basemap_results(**kwargs):

    # Retrieving the arguments
    show = kwargs.get('show', True)
    RDV = kwargs.get('rdv', None)
    BYE = kwargs.get('bye', None);
    A1_orig = kwargs.get('A1_orig', None);
    A1_dest = kwargs.get('A1_dest', None);
    A2_orig = kwargs.get('A2_orig', None);
    A2_dest = kwargs.get('A2_dest', None);
    bounds = kwargs.get('Bounds', None);
    output_file = kwargs.get('out_file', None);
    region = kwargs.get('Region', None);
    
    # Setting the map
    fig = plt.figure(num=1, figsize=(12,12)) 
    map=Basemap(llcrnrlon=region[0],llcrnrlat=region[1],urcrnrlon=region[2],urcrnrlat=region[3])
    map.fillcontinents(color='grey', alpha=0.3, lake_color='grey')
    
    # Plots the position, destination and RDV & BYE points
    Airc_1 = map.plot(A1_orig[0], A1_orig[1], 'b4', markersize=18, label='Aircraft 1')
    Airc_2 = map.plot(A2_orig[0], A2_orig[1], 'r4', markersize=18, label='Aircraft 2')
    Dest_1 = map.plot(A1_dest[0], A1_dest[1], 'bs', markersize=10, label='Destination 1')
    Dest_2 = map.plot(A2_dest[0], A2_dest[1], 'rs', markersize=10, label='Destination 2')
    RDV_point = map.plot(RDV[0], RDV[1], 'ko', markersize=10, label='RDV')
    BYE_point = map.plot(BYE[0], BYE[1], 'kx', markersize=10, label='BYE')
    
    # Draw the boundaries
    p1, p2, p_RDV, p_BYE, d1, d2 = (A1_orig[0],A1_orig[1]), (A2_orig[0],A2_orig[1]), (RDV[0], RDV[1]), (BYE[0], BYE[1]), (A1_dest[0], A1_dest[1]), (A2_dest[0], A2_dest[1])
    plt.fill_between([bounds[0][0],bounds[0][1]], bounds[1][0],bounds[1][1], color='#163A6B', alpha=0.15, label='Boundaries', linewidth=0)
    #[point_set, y_1, y_2] = compute_boundaries_great_circle(p1, p2, p_d, 30)
    #plt.fill_between(point_set, y_1,y_2, color='#163A6B', alpha=0.15, label='Boundaries', linewidth=0)
    
    # Add connections
    line_1_start = map.drawgreatcircle(A1_orig[0],A1_orig[1],RDV[0],RDV[1], linestyle="solid", linewidth=0.6, color='b', label='A1: Cruise alone 1')
    line_2_start = map.drawgreatcircle(A2_orig[0],A2_orig[1],RDV[0],RDV[1], linestyle="solid", linewidth=0.6, color='r', label='A2: Cruise alone 1')
    line_formation = map.drawgreatcircle(RDV[0],RDV[1],BYE[0],BYE[1], linestyle="solid", linewidth=1, color='k', label='Formation flight')
    line_1_end = map.drawgreatcircle(BYE[0],BYE[1],A1_dest[0],A1_dest[1], linestyle="dashdot", linewidth=1, color='b', label='A1: Cruise alone 2')
    line_2_end = map.drawgreatcircle(BYE[0],BYE[1],A2_dest[0],A2_dest[1], linestyle="dashdot", linewidth=1, color='r', label='A2: Cruise alone 2')
    map.drawgreatcircle(A1_orig[0],A1_orig[1],A1_dest[0],A1_dest[1], linestyle="dashdot", linewidth=0.6, alpha=0.5, color='b', label='A1: Alone flight')
    map.drawgreatcircle(A2_orig[0],A2_orig[1],A2_dest[0],A2_dest[1], linestyle="dashdot", linewidth=0.6, alpha=0.5, color='r', label='A2: Alone flight')
    
    # Add arrows
    midpoint_1_start = gcc.intermediate_point(p1, p_RDV, fraction=0.5)
    midpoint_2_start = gcc.intermediate_point(p2, p_RDV, fraction=0.5)
    midpoint_form = gcc.intermediate_point(p_RDV, p_BYE, fraction=0.5)
    midpoint_1_end = gcc.intermediate_point(p_BYE, d1, fraction=0.5)
    midpoint_2_end = gcc.intermediate_point(p_BYE, d2, fraction=0.5)
    add_arrow(line_1_start[0], position=midpoint_1_start)
    add_arrow(line_2_start[0], position=midpoint_2_start)
    add_arrow(line_formation[0], position=midpoint_form)
    add_arrow(line_1_end[0], position=midpoint_1_end)
    add_arrow(line_2_end[0], position=midpoint_2_end)
    
    # Legend
    plt.legend(frameon = True, loc='upper right', edgecolor='1', ncol = 2, borderpad = 1, markerscale = 1.2, labelspacing = 2, facecolor='white')
    
    # Show/hide figure
    if not show: 
        plt.close();
    
    # Saving the file and parameters
    plt.gca().set_axis_off()
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
                hspace = 0, wspace = 0)
    plt.margins(0,0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    fig.savefig(output_file, dpi=900, bbox_inches = 'tight',
        pad_inches = 0, facecolor='w', edgecolor='w', transparent=True, optimize = True, quality=95)
    



    
    



