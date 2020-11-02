#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 1 10:56:31 2020

@author: pierrejablonski
"""

"""
The purpose of this code is save model V.2.3 parameters in a workspace
"""

# Libraires
# --------------
import pickle


# coordinates [long, lat] 
#aircraft_1 = [-87.554420, 41.739685]; # Chicago
#aircraft_1 = [-118.410042, 33.942791]; # Los Angeles
#aircraft_2 = [-73.935242, 40.730610]; # New York
#destination_1 = [2.3488, 48.8534]; # Paris
#aircraft_2 = [-73.935242, 40.730610]; # New York
#aircraft_1 = [-73.567256, 45.5016889]; # Montreal

# -------------- Aircraft 1 flight parameters

aircraft_1 = [-96.808891, 32.779167]; # Dallas
destination_1 = [-3.703790, 40.416775]; # Madrid
equipment_1 = "A333";
W_payload_1 = 43* 10**3; # kg, payload mass example for one flight, Crew + Cargo


A1_flight_params = [aircraft_1, destination_1, equipment_1, W_payload_1];



# -------------- Aircraft 2 flight parameters

aircraft_2 = [-80.191788, 25.761681]; # Miami
destination_2 = [-0.076132, 51.508530]; # London
equipment_2 = "B789";
W_payload_2 = 40* 10**3; # kg, payload mass example for one flight, Crew + Cargo

A2_flight_params = [aircraft_2, destination_2, equipment_2, W_payload_2];



# -------------- Formation flight parameters

alpha = 0.15; # fuel savings efficiency, typically 5-10%

formation_flight_params = [alpha];



# Save to workspace
# -------------- 
f = open('./params.pckl', 'wb')
pickle.dump([formation_flight_params, A1_flight_params, A2_flight_params], f)
f.close()
