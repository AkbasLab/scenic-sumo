# SumoSimulator
### Description 
`SumoSimulator` creates an object that has the map, scenic file, and config file. It creates the simulations and passes them to the scenario information.  
### Syntax  
`simulator(map, scene, config)`
### Parameters
`map`: str: *.sumocfg file for the map  
`scene`: str: *.scenic file for the scenario chosen  
`config`: dict: sumo commands  
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
`scen_num`: int: scene number  
`map`: str: *.sumocfg file for the map  
`scene`: str: *.scenic file for the scenario chosen  
`config`: dict: sumo commands  
### Returns  
None  

---  
## checkForUtilities()
### Description  
`checkForUtilities()`checks for Utility files that will be used in the scene. Random trips and parking lots are done with this.  
### Sytax  
`checkForUtilities(scene, folder_name)`  
### Parameters  
`scene`: tuple: actors in the scene  
`folder_name`: str: folder containing the map  
### Returns  
None 
  
---  
## createParkingLot()
### Desctipition  
`createParkingLot()` creates a parking lot in the scene. Writes to parkinglot.net.xml in Utilities
### Syntax  
`createParkingLot(scenicObj)`  
### Parameters  
`scenicObj`: scenic actor: object containing information from the scene  
### Returns  
None  

---  
## setSumoParam()  
### Description  
`setSumoParam()` gets configuration settings from Utilities/config.py and adds them to terminal command at runtime. Can also be fed any *dict* variable type with Sumo commands.  
### Syntax  
`setSumoParam(sumo_file, sumo_config)`  
### Parameters  
`sumo_file`: str: sumo file name  
`sumo_config`: dict: commands to control the Sumo interface  
### Returns  
:list: commands for the Sumo interface.  

---
## iterateScene()  
### Description  
`iterateScene()` iterates through the scenic object list given from Scenic. It adds less used actors such as the TrafficLight and Pedestrian.  
### Syntax  
`iterateScene(scene)`  
### Parameters  
`scene`: tuple: actors in the Scenic scene  
### Returns  
None  

---  
## createCar()  
### Description  
`createCar()` creates a car in the scene from a scenic object. Count ensures a unique car ID.  
### Syntax  
`createCar(carCount, scenicObj)`  
### Parameters  
`carCount`: int: number of cars in the simulation  
`scenicObj`: model.Car: object containing information to create a car  
### Returns  
None  

---  
## createRandomCar()  
### Description  
`createRandomCar()` creates a car with random attributes that are specified in the scenario. The user must create this object in the scenario with the random ranges specified. Could be expanded upon to support more variables. Currently looking for better alternatives.  
### Syntax  
`createRandomCar(road, scenicObj)`  
### Parameters  
`road`: str: edge which the car spawns on  
`scenicObj`: ___main___.RandomCar: object containing information to create a car with random values  
### Returns  
None  

---  
## createTrafficLight()  
### Description  
`createTrafficLight()` creates a traffic light from the attributes in the scenario.  
### Syntax  
`createTrafficLight(scenicObj)`  
### Parameters  
`scenicObj`: model.TrafficLight: object containing information to change the state of a traffic light  
### Returns  
None  

---  
## createPedestrian()  
### Description  
`createPedestrian()` creates a pedestrian from the attributes in the scenario.  
### Syntax  
`createPedestrian(scenicObj)`  
### Parameters  
`scenicObj`: model.Pedestrian: object containing information to create a pedestrian  
### Returns  
None  

---  
## runSimulation()  
### Description  
`runSimulation()` runs the simulation. While running the simulation it checks for time variables such as changing speed and changing lanes.  
### Syntax  
`runSimulation()`  
### Parameters  
None  
### Returns  
None
