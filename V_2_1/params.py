#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 10:56:31 2020

@author: pierrejablonski
"""

"""
The purpose of this code is save model V.2.3 parameters in a workspace
"""

# Libraires
# --------------
import pickle


# coordinates [long, lat] of aircraft 1 at time of change of course
#aircraft_1 = [-87.554420, 41.739685]; # Chicago
#aircraft_1 = [-118.410042, 33.942791]; # Los Angeles
#aircraft_2 = [-73.935242, 40.730610]; # New York


# -------------- Aircraft 1 flight parameters
aircraft_1 = [-73.567256, 45.5016889]; # Montreal
#aircraft_1 = [-96.808891, 32.779167]; # Dallas
destination_1 = [-0.076132, 51.508530]; # London
fuel_burn_1 = 7; # fuel burn consumption in kg/km or Aircraft 1
equipment_1 = "A333";
W_payload_1 = 43* 10**3; # kg, payload mass example for one flight, Crew + Cargo


A1_flight_params = [aircraft_1, destination_1, fuel_burn_1, equipment_1, W_payload_1];



# -------------- Aircraft 2 flight parameters
aircraft_2 = [-80.191788, 25.761681]; # Miami
#aircraft_2 = [-73.935242, 40.730610]; # New York
destination_2 = [-0.076132, 51.508530]; # London
fuel_burn_2 = 12; # fuel burn consumption in kg/km or Aircraft 2
equipment_2 = "B789";
W_payload_2 = 40* 10**3; # kg, payload mass example for one flight, Crew + Cargo

A2_flight_params = [aircraft_2, destination_2, fuel_burn_2, equipment_2, W_payload_2];



# -------------- Formation flight parameters
destination = [-0.076132, 51.508530]; # London
alpha = 0.15; # fuel savings efficiency, typically 5-10%

formation_flight_params = [destination, alpha];



# Save to workspace
# -------------- 
f = open('./params.pckl', 'wb')
pickle.dump([formation_flight_params, A1_flight_params, A2_flight_params], f)
f.close()
