READ ME FILE - PROJECT FYP 
============================


THE PROJECT 
Route optimisation planner using V-formation flights
------------------------------------------------------------

The purpose of this code is to find several characteristic values (eg. RDV and BYE points) that will best allow several aircrafts to fly in extended formation configurations. Fuel consumption and cost are to be minimized.

Differences with previous version
------------------------------------------------------------

1. Creation of a formation class
2. Differents destinations
3. Timer


VERSION V.2.3
------------------------------------------------------------

**Included**
    * Time constrained: aircraft must meet at RDV (loiter if necessary)
    * 3D space: use of shortest path trajectories
    * Fuel consumption discrete *time-dependent* 
        * Weight fuel fractions 
        * Over 15 steps. 
        * Steps divided in S1, S2, S3 = start, cruise, end
        * S1 fixed: historical values
        * S2 variable: alone or formation_2. Depends on RDV among other params
        * S3 only depends on regulations
    * BYE point
    * Fixed velocity 


**Not included**
        * Varying velocity
        


FILES IN FOLDER
------------------------------------------------------------

1. **Flight class**
    * Creates an object containing parameters and methods about a specific flights
    * Contains aircraft/equipment related parameters
    * Computes S3 (end of flight) fuel fractions based on regulations
    * Creates sub configurations: Alone, Formation 2.
    * Computes S2 (cruise) fuel fractions for each configuration taking another flight object as an argument
    * Solves W0 and Wf (+ other weights required)
    * Derives stats about the flights
    
2. **Maths functions**
    * Contains mathematical functions. 
    * Contains distance functions, fuel fraction functions
    * Contains a Timer class, returning elapsed time during an operation
    
3. **Plot functions**
    * Contains functions producing partial or full plots
    * Elements include: arrows along a flight path, areas filled
    * Full plots include: surface plot 2 DOF inputs for J_f, basemap plot showing flight paths 

4. **Params**
    * Contains parameters used as inputs to run the entire code.
    * Constitutes of typical instances of transatlantic fligths
    * Variables: 2 aircrafts, aircraft type, origin & destination location, formation fuel consumption reduction percentage alpha, payload mass
    
5. **Main**
    * Main file: regroup and executes
    * Steps:
        1. Collects parameters
        2. Instantiates two fligth objects A1 & A2
        3. Run preliminary methods of A1 & A2 + run alone configuration entirely
        4. Bounds are defined (optimization bounds)
        5. Minimize function J_fuel defined
        6. Optimizer is run
        7. Stats displayed
        8. Surface plot run
        9. Basemap run

Outputs produced
------------------------------------------------------------

1. **Stats**
    * Comparison fuel spent and distance with/without formation
    * Loiter? If yes, which aircraft and time duration
    
2. **J_fuel surface plot**
    * Displays a surface plot of the minimize function J_fuel within bounds
    * Shows minimum for the formation picked
    * Only RDV coordinates are taken as inputs. 
    * Note for higher order inputs in the future (i.e. No Inputs > 2), this surface plot will only be a projection
    
3. **Basemap plot**
    * Earth Map showing flight paths
    * Shows RDV
