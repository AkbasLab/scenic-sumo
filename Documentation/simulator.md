# SumoSimulator
### Description 
SumoSimulator creates an object that has the map, scenic file, and config file. It creates the simulations and passes them to the scenario information.  
### Syntax  
`simulator(map, scene, config)`
### Parameters
`map`: str: the *.sumocfg file for the map  
`scene`: str: the *.scenic file for the scenario chosen  
`config`: dict: the dict variable with the desired sumo commands  
### Returns  
None

---
## createSimulation()  
### Description
`createSimulation()` initializes a simulation and adds to the scenario number.  
### Syntax  
`createSimulation()`
### Parameters
None
### Returns  
None  

---
# SumoSimulation  
### Description  
`SumoSimulation` reates a single simulation. Initailizes all the scenic actors and sets up the options for the sumo scene.  
#### Syntax  
`simulation(scen_num, map, scene, config)`  
### Parameters  
`scen_num`: int:  the scene number  
`map`: str: the *.sumocfg file for the map  
`scene`: str: the *.scenic file for the scenario chosen  
`config`: dict: a dict of desired sumo commands  
### Returns  
None  

---  
## checkForUtilities()
### Description  
`checkForUtilities()`checks for Utility files that will be used in the scene. Random trips and parking lots are done with this.  
### Sytax  
`checkForUtilities(scene, folder_name)`  
### Parameters  
`scene`: tuple: A list of the actors in the scene  
`folder_name`: str: the folder containing the map  
### Returns  
None 
  
---  
## createParkingLot()
### Desctipition  
`createParkingLot()` creates a parking lot in the scene.  
### Syntax  
 