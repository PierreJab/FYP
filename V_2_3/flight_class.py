#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 01:22:36 2020

@author: pierrejablonski
"""

"""
The purpose of this code is to create a flight class
"""


"""
class flight methods
    init: 
        - 
        
    class fuel_configuration: 
        - nested class designed to compute fuel fractions depending on w/wo formation
        
    equipment_params: 
        - Import data from the corresponding type of aircraft
        
        
    compute_other_aero_quantities:
        - Uses aircraft data imported to compute other quantities


"""


#import pprint
import traceback
import pandas as pd
import sys
import math as m
import numpy as np
from colorama import Fore
from colorama import Style
from ambiance import Atmosphere

from maths_func import haversine_distance, compute_W_ff_cruise, compute_W_ff_loiter, W_ff_up_2_step_p, W_ff_cumul, V_imD

class flight:

    def __init__(self, equipment, orig, dest, W_payload, *args, **kwargs):
        # Getting the name of the instance
        (filename,line_number,function_name,text)=traceback.extract_stack()[-2]
        def_name = text[:text.find('=')].strip()
        self.name = def_name
        
        # Instantiating arguments
        self.equipment = equipment;
        self.orig = orig;
        self.dest = dest;
        self.W_payload = W_payload;
        
        # Instantiate fixed parameters
        self.fuel_margin = 0.06; # %, accounts for reserve and trapped fuel
        self.phi_loiter = 10; # deg, turn angle during loiter (assumed constant)
        self.E_loiter_1 = 0.5; # hour, endurance required by FAR-25 for loiter 1
        self.R_V_divert = 0.5; # hour, endurance equivalent to R/V required by FAR-25 for divert
        self.E_loiter_2 = 0.5; # hour, endurance required by FAR-25 for loiter 2
        
        # Instantiate equipment & configurations obj
        self.aircraft = self.Aircraft(self);
        self.alone = self.fuel_configuration(1);
        self.formation_2 = self.fuel_configuration(2);
        
        # Instantiating with the arguments passed and defined
        for key, value in kwargs.items():
            setattr(self, key, value)
        
#        print(Fore.BLUE, u'\u2713', self.name, ':', "Initialisation done", Style.RESET_ALL)
                   
    def __str__(self):
        print('\n', '---------------', self.name)
        for key in self.__dict__:
            print('   ', key, ':', self.__dict__[key])
        return "end ---------------------------"
#        return str(pprint.pprint(self.__dict__))
        
    
    
    
    
    class Aircraft:
        
        def __init__(self, obj):
            self.type = obj.equipment;
            self.phi_loiter = 10; # deg, turn angle during loiter (assumed constant)
            
            # Getting the name of the instance
            (filename,line_number,function_name,text)=traceback.extract_stack()[-2]
            def_name = text[:text.find('=')].strip()
            self.name = def_name
            
        def __str__(self):
            c = 0;
            for key in self.__dict__:
                if c == 0:
                    print('\n   ', '   ', key, ':', self.__dict__[key])
                else:
                    print('   ', '   ', key, ':', self.__dict__[key])
                c += 1;
            return ""
        
        def populate(self):
        
            # Open csv
            try:
                # Note the relative path is based on a use from the model scripts folder
                df = pd.read_csv("../../DB/equipment_DB/equipment_data.csv", delimiter=";", decimal=",", encoding="latin1")
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
                
            # Find the row in the database that corresponds to the equipment
            try: 
                row = df[df['Equipment'].str.match(self.type)]
                if len(row) == 0:
                    print(Fore.RED, 'x', 'Error: Equipment not found', Style.RESET_ALL)
                    raise Exception("Error: Equipment not found")
                elif len(row) > 1:
                    row.drop_duplicates(subset=['equipment'], keep='first', inplace=True)
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
            
            # Instantiate with data
            try: 
                self.k = row["Wing inefficiency k"].values[0];
                self.CD_0 = row["CD_0"].values[0];
                self.S = row["Wing surface, m2"].values[0];
                self.b = row["Span, m"].values[0];
                self.AR = row["Aspect ratio"].values[0];
                self.M_cruise = row["Mach cruise"].values[0];
                self.h_cruise = row["Altitude cruise, m"].values[0];
                self.SFC_cruise = row["SFC cruise, /hr"].values[0];
                self.SFC_loiter = row["SFC loiter, /hr"].values[0];
                self.MTOW = row["MTOW, kg"].values[0];
                self.OEW = row["OEW, kg"].values[0];
                self.MLW = row["MLW, kg"].values[0];
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
                

        def compute_other_aero_quantities(self):
            
            # Compute cruise speed, based on altitude and Mach during cruise
            V_sound = Atmosphere(int(self.h_cruise)).speed_of_sound[0]; # h_cruise must be in meters
            self.V_cruise = round(self.M_cruise * V_sound, 1); # m/s
            
            # Compute (L/D)_max
            self.L_D_max = round(0.5 * m.sqrt(m.pi * self.AR / (self.k * self.CD_0)), 2);
            
            # Compute load factor during loiter
            self.n_loiter = round(1/m.cos(self.phi_loiter*2*m.pi/360), 4);
    
    
    
    
    
    class fuel_configuration:
        
        def __init__(self, n):
            
            # Getting the name of the instance
            (filename,line_number,function_name,text)=traceback.extract_stack()[-2]
            def_name = text[:text.find('=')].strip()
            self.name = def_name
            self.n = n;
            
            # Instantiate fuel fraction in formation or alone
            self.W_ff_start = [0.99, 0.99, 0.995, 0.985];
            self.W_ff_end = [0, 0.995, 1, 0.985, 0, 0, 0.995, 1, 0.99];
            self.W_ff_cruise = [];
            
            
        def __str__(self):
            c = 0;
            for key in self.__dict__:
                if c == 0:
                    pass;
                elif c == 1:
                    print('\n   ', '   ', key, ':', self.__dict__[key])
                else:
                    print('   ', '   ', key, ':', self.__dict__[key])
                c += 1;
            return ' '
        
            
        def compute_W_ff_end(self, obj):
            # Loiter 1
            self.W_ff_end[0] = round(compute_W_ff_loiter(obj.E_loiter_1, obj.aircraft.SFC_loiter, obj.aircraft.L_D_max), 3);
            
            # Divert
            # R = 0.75, V = 1, because we need R/C = 0.75 i.e. 45 minutes as per the FAR-25 regulations
            self.W_ff_end[4] = round(compute_W_ff_cruise(obj.R_V_divert, obj.aircraft.SFC_cruise, 1, 0.866*obj.aircraft.L_D_max), 3)
            
            # Loiter 2
            self.W_ff_end[5] = round(compute_W_ff_loiter(obj.E_loiter_2, obj.aircraft.SFC_loiter, obj.aircraft.L_D_max), 3)

        
        def compute_W_ff_cruise(self, obj, **kwargs):
            
            if self.n == 1:
                self.distance_total = haversine_distance(obj.orig[0], obj.orig[1], obj.dest[0], obj.dest[1]);
                fuel_frac_alone = round(compute_W_ff_cruise(self.distance_total, obj.aircraft.SFC_cruise, obj.aircraft.V_cruise*3.6, 0.866*obj.aircraft.L_D_max),3);
                self.W_ff_cruise.append(fuel_frac_alone);
        
            elif self.n == 2:
                
                # Retrieving the vector as an argument
                x = kwargs.get('vector', None)
                A_other = kwargs.get('A_other', None)
                alpha = kwargs.get('alph', None)
                
                # House-keeping: starting over, re-initialisation
                self.W_ff_cruise = [];
                                
                self.l1_bf = haversine_distance(obj.orig[0], obj.orig[1], x[0], x[1]);
                self.l2_bf = haversine_distance(A_other.orig[0], A_other.orig[1], x[0], x[1]);
                self.l_f = haversine_distance(x[0], x[1], x[2], x[3]);
                self.l1_af = haversine_distance(x[2], x[3], obj.dest[0], obj.dest[1]);
                self.l2_af = haversine_distance(x[2], x[3], A_other.dest[0], A_other.dest[1]);
                
                self.t1 = self.l1_bf / (obj.aircraft.V_cruise*3.6);
                self.t2 = self.l2_bf / (A_other.aircraft.V_cruise*3.6);
                self.V_f = min(obj.aircraft.V_cruise, A_other.aircraft.V_cruise)*3.6; # formation velocity
                
                # cruise alone 1
                cruise_alone_1 = round(compute_W_ff_cruise(self.l1_bf, obj.aircraft.SFC_cruise, obj.aircraft.V_cruise*3.6, 0.866*obj.aircraft.L_D_max), 3);
                self.W_ff_cruise.append(cruise_alone_1);
                
                # loiter alone
                if min(self.t1,self.t2) == self.t1:  
                    self.must_loiter_formation = True;
                    loiter_alone = round(compute_W_ff_loiter(abs(self.t2-self.t1), obj.aircraft.SFC_loiter, obj.aircraft.L_D_max),3);
                    self.W_ff_cruise.append(loiter_alone);
                
                # cruise formation 
                W_frac_1_temp = compute_W_ff_cruise(self.l_f, obj.aircraft.SFC_cruise, self.V_f, 0.866*obj.aircraft.L_D_max);
                cruise_formation = round((1-(1-W_frac_1_temp)*(1-alpha)),3);
                self.W_ff_cruise.append(cruise_formation);
                
                # cruise alone 2
                cruise_alone_2 = round(compute_W_ff_cruise(self.l1_af, obj.aircraft.SFC_cruise, obj.aircraft.V_cruise*3.6, 0.866*obj.aircraft.L_D_max), 3);
                self.W_ff_cruise.append(cruise_alone_2);
                
                
        def solve_weights(self, obj):
            self.W_ff = self.W_ff_start + self.W_ff_cruise + self.W_ff_end; # assemble fuel fraction array
            self.W_ff_total = round(np.prod(self.W_ff),3) # Total flight weight fraction
            self.Wf_W0 = round((1+obj.fuel_margin)*(1-self.W_ff_total),3); #Actual Fuel fraction with fuel margin
            self.W0 = round((obj.aircraft.OEW + obj.W_payload)/(1-self.Wf_W0))
            self.Wf = round(self.Wf_W0 * self.W0);
            self.TOW = round(self.W0*W_ff_up_2_step_p(self.W_ff, 3));
            self.W_steps = np.around(self.W0*np.array(W_ff_cumul(self.W_ff)), decimals=0);
            
        def stats(self, obj):
            
            self.TOW_margin = round(self.TOW/obj.aircraft.MTOW *100, 1) # percentage TOW/MTOW
            
            # Fuel spent on regular trip
            ff_no_pb = np.prod(self.W_ff_start) * np.prod(self.W_ff_cruise) * np.prod(self.W_ff_end[-3:-1] + [self.W_ff_end[-1]])
            self.W_fuel_spent_wo_pb = round(self.W0 * (1 - ff_no_pb));
            
            # Fuel spent using emergency fuel
            self.W_fuel_spent_w_pb = round(self.W0 - self.W_steps[-1]);
            
            # Loiter velocity V_imD in m/s
            i_loiter_1 = len(self.W_ff_start) + len(self.W_ff_cruise) - 2
            i_loiter_2 = i_loiter_1 + 5;
            W_loiter_1 = self.W_steps[i_loiter_1];
            W_loiter_2 = self.W_steps[i_loiter_2];
            self.V_imD_loiter_1 = round(V_imD(obj.aircraft.n_loiter, W_loiter_1*9.81, obj.aircraft.S, obj.aircraft.k, obj.aircraft.AR, obj.aircraft.CD_0, 1.225), 2);
            self.V_imD_loiter_2 = round(V_imD(obj.aircraft.n_loiter, W_loiter_2*9.81, obj.aircraft.S, obj.aircraft.k, obj.aircraft.AR, obj.aircraft.CD_0, 1.225), 2);
            
            if self.n == 1:
                # total distance in km
                self.distance_total = round(haversine_distance(obj.orig[0], obj.orig[1], obj.dest[0], obj.dest[1]))
                
            elif self.n ==2:
                
                # If Loiter : must & time in hour
                if ((min(self.t1,self.t2) == self.t1) & (abs(self.t1 - self.t2) > 0.01)):  
                    self.must_loiter_formation = True;
                    
                    # Loiter alone velocity V_imD in m/s
                    W_loiter_alone = self.W_steps[len(self.W_ff_start) + 2 - 2];
                    self.V_imD_loiter_alone = round(V_imD(obj.aircraft.n_loiter, W_loiter_alone*9.81, obj.aircraft.S, obj.aircraft.k, obj.aircraft.AR, obj.aircraft.CD_0, 1.225), 2);
                    
                else:
                    self.must_loiter_formation = False;
                self.loiter_time = round(abs(self.t2-self.t1), 3) if self.must_loiter_formation else 0
                
                # total distance in km
                self.distance_total = round(self.l1_bf + self.l_f + self.l1_af,1)
                
        
    
