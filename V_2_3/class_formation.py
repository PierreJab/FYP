#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 01:44:46 2020

@author: pierrejablonski
"""

import traceback

class formation:

    def __init__(self, A1, A2, alpha, n, *args, **kwargs):
        # Getting the name of the instance
        (filename,line_number,function_name,text)=traceback.extract_stack()[-2]
        def_name = text[:text.find('=')].strip()
        self.name = def_name
        
        # Instantiating arguments
        self.A1 = A1;
        self.A2 = A2;
        self.alpha = alpha;
        self.n = n;
                
        # Instantiate equipment & configurations obj
        self.stats = self.Stats();
        
        # Instantiating with the arguments passed and defined
        for key, value in kwargs.items():
            setattr(self, key, value)
        
                   
    def __str__(self):
        print('\n', '---------------', self.name)
        for key in self.__dict__:
            if (key == "A1" or key == "A2"):
                continue
            print('   ', key, ':', self.__dict__[key])
        return "end ---------------------------"
    
    class Stats:
        
        def __init__(self):
            # Getting the name of the instance
            (filename,line_number,function_name,text)=traceback.extract_stack()[-2]
            def_name = text[:text.find('=')].strip()
            self.name = def_name
        
        def __str__(self):
            print('\n', '---------------', self.name)
            for key in self.__dict__:
                print('   ', key, ':', self.__dict__[key])
            return "end ---------------------------"
        
        def time(self, obj1, obj2):
            
            # Distance
            self.distance_alone = obj1.alone.distance_total + obj2.alone.distance_total
            self.distance_form = obj1.formation_2.distance_total + obj2.formation_2.distance_total
            # Positive means extra distance, negative means less distance
            self.distance_extra = round((self.distance_form-self.distance_alone)/self.distance_alone, 4)
            
            # Fuel spent
            self.fuel_spent_alone = obj1.alone.W_fuel_spent_wo_pb + obj2.alone.W_fuel_spent_wo_pb;
            self.fuel_spent_form = obj1.formation_2.W_fuel_spent_wo_pb + obj2.formation_2.W_fuel_spent_wo_pb;
            # Positive means savings, negative means extra consumption
            self.fuel_spent_saved = round((self.fuel_spent_alone - self.fuel_spent_form)/self.fuel_spent_alone, 4);
            
            # Time
            self.total_time_alone_1 = round(obj1.alone.distance_total / (obj1.aircraft.V_cruise*3.6), 2);
            self.total_time_alone_2 = round(obj2.alone.distance_total / (obj2.aircraft.V_cruise*3.6), 2);
            self.total_time_alone = self.total_time_alone_1 + self.total_time_alone_2;
            
            self.total_time_form_1 = round(obj1.formation_2.t1 + obj1.formation_2.l_f / obj1.formation_2.V_f + obj1.formation_2.l1_af/(obj1.aircraft.V_cruise *3.6), 2);
            self.total_time_form_2 = round(obj2.formation_2.t1 + obj2.formation_2.l_f / obj2.formation_2.V_f + obj2.formation_2.l1_af/(obj2.aircraft.V_cruise *3.6), 2);
            self.total_time_form = self.total_time_form_1 + self.total_time_form_2;
            self.time_extra_A1 = round((self.total_time_form_1 - self.total_time_alone_1)/self.total_time_alone_1, 2);
            self.time_extra_A2 = round((self.total_time_form_2 - self.total_time_alone_2)/self.total_time_alone_2, 2);
            self.time_extra_form = round((self.total_time_form - self.total_time_alone)/self.total_time_alone, 2);
            
            
            # Loiter time
            self.loiter_time = round(obj1.formation_2.loiter_time + obj2.formation_2.loiter_time, 2)
            self.loiter_A1 = False;
            self.loiter_A2 = False;
            if not (round(obj1.formation_2.loiter_time,2)  == 0):
                self.loiter_A1 = True;
            elif not (round(obj2.formation_2.loiter_time,2)  == 0):
                self.loiter_A2 = True;
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        