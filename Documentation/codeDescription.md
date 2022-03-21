# Scenic-Sumo
The integration of scenic and sumo.

- [Scenic Github](https://github.com/BerkeleyLearnVerify/Scenic)  
- [SUMO Documentation](https://sumo.dlr.de/docs/TraCI.html)
- [GUI Documentation](https://pysimplegui.readthedocs.io/en/latest/)
- [Real Maps](https://www.openstreetmap.org/search?query=hello#map=16/10.4427/-3.1252)

---
## Files  
### Simulator.py  
The simulator file is the core of the integration of Scenic and Sumo. The function of this file is to create a simulator that in turn creates simulations. This is called when the user clicks run in the interface.

All of the functionaity of the actors in the scene are set in *SumoSimulation*. The simulation class creates each actor by iterating through a list of scenic objects that are pulled from *.scenic scenarios. When adding a new actor or variable in model.scenic, it must be added here as well and be translated to a traci function.  

Utility files are also called from *SumoSimulation*. Utility files are files that will be used in specific instances and are toggled in the *config.py* file. For example, *randomTrips.py* is only used when the user uncomments the random trips option in the *config.py* file.

### Model.scenic
This contains the base values for all scenic scenarios. If a car is created than it will have all the defualt values of the object in this file. 

### Interface.py  
This creates all the user interfaces.

### Config.py
This is the command line options for SUMO. This file dictates what is available in the *Sumo Configurator* scene. If the line is commented out in the *Config.py* file than it will not appear in the scene. To find more arguments for this file go [here](https://github.com/crumpl07/ScenicSumo/blob/main/Documentation/sumo-help.txt).

### Map Files
Map files are specific to your computer. They need to be recompiled when using a different computer. Map files are named 

---  
## Current Problems :)

* When a car is created on a route with a random distance value along its route than it will stop on the starting edge. To recreate this issue, run this [file](https://github.com/crumpl07/ScenicSumo/blob/Luke/Scenarios/OnRamp.scenic).
* The *Sumo Configuratior* scene needs to be saved before every run. Should be able to run without clicking save in the scene before running. Should also add a boolean to add or not add a parameter so the user doesn't have to edit the config.py scene directly.