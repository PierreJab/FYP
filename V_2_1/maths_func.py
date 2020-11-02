#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 22:28:31 2020

@author: pierrejablonski
"""


"""
This file contains mathematics functions for the purpose of V-Formation Masters Thesis
"""

# Librairies
# --------------
import math as m
from math import radians
import numpy as np
from sklearn.metrics.pairwise import haversine_distances
import great_circle_calculator.great_circle_calculator as gcc


# Haversine function, computes the distance between two points on the great circle
def haversine_distance(orig_long, orig_lat, dest_long, dest_lat):
    origin_coord = [orig_lat, orig_long]
    destination_coord = [dest_lat, dest_long]
#    origin_in_radians = [radians(_) for _ in origin_coord]
    origin_in_radians = np.radians(origin_coord)
#    destination_in_radians = [radians(_) for _ in destination_coord]
    destination_in_radians = np.radians(destination_coord)
    res = haversine_distances([origin_in_radians, destination_in_radians])[0][1] * 6371000/1000
    return res



# Intermediate points on a great circle trajectory
def points_on_great_circle(p_orig, p_dest, n):
    x_array = []; # long
    y_array = []; # lat
    for i in range(n):
        point = gcc.intermediate_point(p_orig, p_dest, fraction=i/(n-1))
        x_array.append(point[0])
        y_array.append(point[1])
    return [x_array, y_array];


def W_ff_up_2_step_p(array, p):
    res = 1;
    for i in range(p):
        res *= array[i];
    return res;

def W_ff_cumul(array):
    res = [];
    k = 1;
    for i in range(len(array)):
        k *= array[i];
        res.append(k)
    return res;




# The following functions are future methods that will belong to the aircraft class
# they should be computed at instantiation

def compute_W_ff_cruise(R, C, V, L_D):
    # R range in km, C specific fuel consumption in /hr, V velocity in km/hr
    return m.exp(-R*C/(V*L_D));


def compute_W_ff_loiter(E, C, L_D):
    # E endurance in hr, C specific fuel consumption in /hr
    return m.exp(-E*C/L_D);

def V_imD(n, W, S, k, AR, CD_0, rho_0):
    return m.sqrt(n) * m.sqrt(2*W/(rho_0 * S)) * (k/(m.pi * AR * CD_0))**(1/4)