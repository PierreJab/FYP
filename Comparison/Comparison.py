#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 23:11:00 2020

@author: pierrejablonski
"""


"""
This code tries aims at comparing the different model best RDV point for minimum fuel consumed. 
It starts by taking the fuel consumption without formation flights. 
"""

# Libraires
# --------------

import pickle

import sys
sys.path.append('../Functions')
from maths_func import haversine_distance


# Retrieving data
f = open('./workspaces/res_V01_3.pckl', 'rb')
RDV_hvs, fuel_spent_hvs, total_distance_hvs = pickle.load(f)
f.close()

# Retrieving data
f = open('./workspaces/res_V02_1.pckl', 'rb')
RDV_V02, fuel_spent_V02, total_distance_V02 = pickle.load(f)
f.close()

# Parameters
# --------------
f = open('./workspaces/params_V01s.pckl', 'rb')
alpha, fuel_burn_1, fuel_burn_2, aircraft_1, aircraft_2, destination = pickle.load(f)
f.close()


# Non-optimised problem
# Straight distance from Aircraft 1 or 2 to destination
L1 = haversine_distance(aircraft_1[0], aircraft_1[1], destination[0], destination[1]) 
L2 = haversine_distance(aircraft_2[0], aircraft_2[1], destination[0], destination[1])
fuel_non_opt = fuel_burn_1 * L1 + fuel_burn_2 * L2;
distance_non_opt = L1 + L2;

# Savings/losses percentage
fuel_saved_V3 = (fuel_spent_hvs - fuel_non_opt)/fuel_non_opt;
fuel_saved_V02 = (fuel_spent_V02 - fuel_non_opt)/fuel_non_opt;



distance_extra_V3 = (total_distance_hvs - distance_non_opt)/distance_non_opt
distance_extra_V02 = (total_distance_V02 - distance_non_opt)/distance_non_opt

# Display
print('\n')
print('Total fuel spent without formation: ', round(fuel_non_opt/100)/10, 't')
print('Total fuel spent V.0.1.1: ', 'N/A, coordinates not in km')
print('Total fuel spent V.0.1.2: ', 'N/A, coordinates not in km')
print('Total fuel spent V.0.1.3: ', round(fuel_spent_hvs/100)/10, 't')
print('Total fuel spent V.0.2.1: ', round(fuel_spent_V02/100)/10, 't')
print('\n')
print('Total fuel savings V.0.1.3: ', round(fuel_saved_V3*1000)/10, '%')
print('Total fuel savings V.0.2.1: ', round(fuel_saved_V02*1000)/10, '%')
print('\n')
print('Total distance without formation: ', round(distance_non_opt), 'km')
print('Total distance V.0.1.1: ', 'N/A, coordinates not in km')
print('Total distance V.0.1.2: ', 'N/A, coordinates not in km')
print('Total distance V.0.1.3: ', round(total_distance_hvs), 'km')
print('Total distance V.0.2.1: ', round(total_distance_V02), 'km')
print('\n')
print('Extra distance V.0.1.3: ', round(distance_extra_V3*1000)/10, '%')
print('Extra distance V.0.2.1: ', round(distance_extra_V02*1000)/10, '%')
print('\n')







