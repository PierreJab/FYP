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









