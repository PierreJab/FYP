#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 13:49:27 2020

@author: pierrejablonski
"""

"""
The purpose of this code is to save in a workspace to parameters usefull to models of version V_0_1_n
"""

# Libraires
# --------------
import pickle

# Parameters
# --------------

alpha = 0.05; # fuel savings efficiency, typically 5-10%
fuel_burn_1 = 7; # fuel burn consumption in kg/km or Aircraft 1
fuel_burn_2 = 12; # fuel burn consumption in kg/km or Aircraft 2

# coordinates [long, lat] of aircraft 1 at time of change of course
aircraft_1 = [-87.554420, 41.739685]; # Chicago
aircraft_1 = [-73.567256, 45.5016889]; # Montreal
#aircraft_1 = [-118.410042, 33.942791]; # Los Angeles

# coordinates of aircraft 2 at time of change of course
aircraft_2 = [-80.191788, 25.761681]; # Miami
aircraft_2 = [-73.935242, 40.730610]; # New York

# coordinates of destination
destination = [-0.076132, 51.508530]; # London




# Save to workspace
f = open('./params.pckl', 'wb')
pickle.dump([alpha, fuel_burn_1, fuel_burn_2, aircraft_1, aircraft_2, destination], f)
f.close()


