# Scenic-Sumo
The integration of scenic and sumo.

- [Scenic Github](https://github.com/BerkeleyLearnVerify/Scenic)  
- [SUMO Documentation](https://sumo.dlr.de/docs/TraCI.html)
- [GUI Documentation](https://pysimplegui.readthedocs.io/en/latest/)
- [Real Maps](https://www.openstreetmap.org/search?query=hello#map=16/10.4427/-3.1252)

---
# Installation
## Python Version   
Python 3.8 is used because 3.9 is not supported at the time of creating this project. To download 3.8 follow this [link](https://www.python.org/downloads/release/python-3810/).  

## Scenic  
For a full guide to install Scenic click [here](https://scenic-lang.readthedocs.io/en/latest/quickstart.html). Install Scenic with the following command:  
```pip install scenic```  

## Installing Sumo  
Click [here](https://www.eclipse.org/sumo/) to install SUMO. Help with interfacing  TraCI from Python can be found [here](https://sumo.dlr.de/docs/TraCI/Interfacing_TraCI_from_Python.html). If you encounter an issue with the SUMO_HOME variable not being declared click [here](https://sumo.dlr.de/docs/Basics/Basic_Computer_Skills.html#additional_environment_variables).  

## Setting Up Simulator  
To incorporate this project with the Scenic library you have to place this project in this path: ```scenic\simulators\sumo```. To finish the set up, the *.sumocfg files will need to be recompiled to have your path. To reconfigure a map file open the *.net.xml file that has the same name as the desired map file. Under ```Edit``` select ```Open in sumo-gui```. Save the *.sumocfg file by clicking ```Save Configuration``` under ```File```. This will change the path of the file to your computer so an error is not thrown. This will need to be done for every map file that is used. 

--- 
## Files  
This section is an overview of what the files do in the system.
### Simulator.py  
The simulator file is the core of the integration of Scenic and Sumo. The function of this file is to create a simulator that in turn creates simulations. This is called when the user clicks run in the interface.

All of the functionaity of the actors in the scene are set in *SumoSimulation*. The simulation class creates each actor by iterating through a list of scenic objects that are pulled from *.scenic scenarios. When adding a new actor or variable in model.scenic, it must be added here as well and be translated to a traci function.  

Utility files are also called from *SumoSimulation*. Utility files are files that will be used in specific instances and are toggled in the *config.py* file. For example, *randomTrips.py* is only used when the user uncomments the random trips option in the *config.py* file. The randomTrips.py creates a trips.trips.xml file in the same directory that the user starts the simulation. This will be overwirtten if a new map is chosen.

### Model.scenic
This contains the base values for all scenic scenarios. If a car is created than it will have all the defualt values of the object in this file. The name and the route of every object must be given for SUMO to run properly. 

### Interface.py  
This creates all the user interfaces. The sumo configurator scene needs to be saved before running any simulation. Below are all the interface scenes:  
![alt text](https://github.com/AkbasLab/scenic-sumo/blob/main/Documentation/Pictures/SumoScenicHome.PNG)  
   
![alt text](https://github.com/AkbasLab/scenic-sumo/blob/main/Documentation/Pictures/SumoScenicHomeOptions.PNG)  
   
![alt text](https://github.com/AkbasLab/scenic-sumo/blob/main/Documentation/Pictures/ScenicSumoFileBrowser.PNG)  
   
![alt text](https://github.com/AkbasLab/scenic-sumo/blob/main/Documentation/Pictures/SumoScenicConfig.PNG)

### Config.py
This is the command line options for SUMO. This file dictates what is available in the *Sumo Configurator* scene. If the line is commented out in the *Config.py* file than it will not appear in the scene. To find more arguments for this file go [here](https://github.com/AkbasLab/scenic-sumo/blob/main/Documentation/sumo-help.txt).

### Map Files
Map files are specific to your computer. They need to be recompiled when using a different computer.

---  
## Current Problems :)

* When a car is created on a route with a random distance value along its route than it will stop on the starting edge. To recreate this issue, run this [file](https://github.com/AkbasLab/scenic-sumo/blob/main/Scenarios/OnRamp.scenic). Need to look into 
* The *Sumo Configuratior* scene needs to be saved before every run. Should be able to run without clicking save in the scene before running. Should also add a boolean to add or not add a parameter so the user doesn't have to edit the config.py scene directly.