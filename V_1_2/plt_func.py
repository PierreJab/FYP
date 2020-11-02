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

import sys
sys.path.append('../Functions')
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







