READ ME FILE - PROJECT FYP 
============================


THE PROJECT 
Route optimisation planner using V-formation flights
------------------------------------------------------------

The purpose of this code is to find several characteristic values (eg. RDV and BYE points) that will best allow several aircrafts to fly in extended formation configurations. Fuel consumption and cost are to be minimized.

Differences with previous version
------------------------------------------------------------

1. 3D space problem using shortest path trajectories


VERSION V.1.3
------------------------------------------------------------

**Included**
    * 3D space: space problem using haversine functions
    * Fixed fuel consumption using fuel burns
        * Fuel burn per aircraft
    * Linear bounds in optimizer
    * Fixed velocity 


**Not included**
        * Not time constrained: aircraft don't actually *meet* at RDV


FILES IN FOLDER
------------------------------------------------------------
    
1. **Maths functions**
    * Contains mathematical functions. 
    * Contains distance functions
    
2. **Plot functions**
    * Contains functions producing partial or full plots
    * Elements include: arrows along a flight path, areas filled

3. **Params**
    * Contains parameters used as inputs to run the entire code.
    * Constitutes of typical instances of transatlantic fligths
    * Variables: 2 aircrafts, origin location, formation, alpha_formation, fuel burn
    
4. **Main**
    * Main file: regroup and executes
    * Steps:
        1. Collects parameters
        2. Bounds are defined (optimization bounds)
        3. Minimize function J_fuel defined
        4. Optimizer is run
        5. Basemap run

Outputs produced
------------------------------------------------------------

1. **Basemap plot**
    * Earth Map showing flight paths
    * Shows RDV
