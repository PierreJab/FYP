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
from math import radians
from sklearn.metrics.pairwise import haversine_distances
import great_circle_calculator.great_circle_calculator as gcc


# Haversine function, computes the distance between two points on the great circle
def haversine_distance(orig_long, orig_lat, dest_long, dest_lat):
    origin_coord = [orig_lat, orig_long]
    destination_coord = [dest_lat, dest_long]
    origin_in_radians = [radians(_) for _ in origin_coord]
    destination_in_radians = [radians(_) for _ in destination_coord]
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


