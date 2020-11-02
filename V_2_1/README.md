READ ME FILE - PROJECT FYP 
============================


THE PROJECT 
Route optimisation planner using V-formation flights
------------------------------------------------------------

The purpose of this code is to find several characteristic values (eg. RDV and BYE points) that will best allow several aircrafts to fly in extended formation configurations. Fuel consumption and cost are to be minimized.

Differences with previous version
------------------------------------------------------------

1. Equipment type data (aero params such as k, AR, SFC_loiter, S, M_cruise...)
2. Loiter at RDV to impose time-constraints


VERSION V.2.1
------------------------------------------------------------

**Included**
    * Time constrained: aircraft must meet at RDV (loiter if necessary)
    * 3D space: use of shortest path trajectories
    * Fixed fuel consumption using fuel burn.  
        * Fuel burn per aircraft
    * Fixed velocity 


**Not included**
        * Time-evolutive fuel consumption


FILES IN FOLDER
------------------------------------------------------------
    
1. **Maths functions**
    * Contains mathematical functions. 
    * Contains distance functions, fuel fraction functions
    
3. **Plot functions**
    * Contains functions producing partial or full plots
    * Elements include: arrows along a flight path, areas filled

4. **Params**
    * Contains parameters used as inputs to run the entire code.
    * Constitutes of typical instances of transatlantic fligths
    * Variables: 2 aircrafts, aircraft type, origin location, alpha_formation, fuel burn
    
5. **Main**
    * Main file: regroup and executes
    * Steps:
        1. Collects parameters
        2. Bounds are defined (optimization bounds)
        3. Minimize function J_fuel defined
        4. Optimizer is run
        5. Stats displayed
        6. Basemap run

Outputs produced
------------------------------------------------------------

1. **Stats**
    * Comparison fuel spent and distance with/without formation
    * Loiter? If yes, which aircraft and time duration

2. **Basemap plot**
    * Earth Map showing flight paths
    * Shows RDV
