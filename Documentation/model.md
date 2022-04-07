## Car Object
The car object allows the user to create a car and give a route to follow through the simulation. An example of each attribute is given below.

```
Car = Car at 0 @ 0
```  
Instantiates the object. 

```
Car.name = "carName"
```  
The car name must be unique.

```
Car.route = ["startRoad", "endRoad"]
```  
The road names can be found in the *.net.xml files when clicking on the edges. To make a specific route add more road names between startRoad and endRoad.

```
Car.distance = 10
```  
Sets the spawn distance from the node at which the car spawns.

```
Car.lane = 0
```  
Specifies the lane to spawn the vehicle on when the road has more than 1 lane.

```
Car.laneMode = 0
```
Specifies the options for lane changing in the scene. More can be found [here](https://sumo.dlr.de/docs/TraCI/Change_Vehicle_State.html#lane_change_mode_0xb6).

```
Car.xPos = 0
```  
Specifies the x position. Point 0,0 cannot be used, otherwise vehicle will spawn at regular spawn node.

```
Car.yPos = 0
```  
Specifies the y position.

```
Car.angle = 10
```  
Specifies the spawn angle of the car. Will change after the car enters the route.

```
Car.vehPlacement = 1
```  
Specifies how the car will be placed in the scene. If not specified than option 1 will be chosen.  
> 0 - The car will be placed on any edge and the edge will be the vehicles route.  
> 1 - The car will be placed on the nearest edge to from the x and y position given.  
> 2 - The car will be placed on the coordinates given.  

```
Car.speed = 10
```  
Sets the cars speed to the value given. If speed is -1 than the car will assume the speed given by the road it is on.  

```
Car.changeSpeed = [10, 3, 10]
```  
Specifies the new speed of the vehicle and the amount of time to change to that speed. The last value is the time in the simulation at which the vehicle will start to slow down. [speed, time, simTime]

```
Car.track = 0
```
Sets the gui to track the car. If not specified than option 0 will be chosen.  
> 0 - The car will not be tracked.  
> 1 - The car will be tracked buy the gui.

```
Car.color = [255,0,0,255]
```  
Sets the color for the highlight on a car. The color given above is red.

```
Car.size = 5
```  
Sets the size of the highlight circle. The preset is 5.  

```
Car.speedMode = 32
```  
Sets what the vehicle will ignore such as red lights, and maximum acceleration limits. 32 will allow the vehicle to ignore all laws and limits set by SUMO. More can be found [here](https://sumo.dlr.de/docs/TraCI/Change_Vehicle_State.html#speed_mode_0xb3).  

```
Car.tau = 0.1
```  
Sets the reaction time of the driver in the simulation. Any value below the step size will result in a delayed response by the driver and may lead to collisions.  

```
Car.carParam = 1
```
Allows the car to have collisions at intersections. The --collision.check-junctions option in the config.py file must be activated as well for a car to have a collision at an intersection.  

```
Car.parkPos = ["parkingLotName", 10]
```  
The car will park in the parking lot given for the amount of time specified.  

## Traffic Light Object
The traffic light object allows the user to create a traffic light in the scene and set the phases of the traffic light. The traffic light object controls sidewalks as well. The traffic light attribute examples are as follows:

```
tL = TrafficLight at 0 @ 0
```  
Instantiates the object. 

```
tL.name = "trafficLight"
```  
The names for the lights must be unique.

```
tL.state = "GGGgrrrrGGGgrrrr,yyyyrrrryyyyrrrr,rrrrGGGgrrrrGGGg"
```  
Each string of letters separated by a comma represents one state that the traffic light will do. The size of the string may be smaller or larger for different kinds of traffic lights. For example, an intersection with three roads and one lane for each would be smaller than an intersection with four roads and two lanes for each road.  
> G - denotes a right of way green light  
> g - denotes a turning light in which the driver must check traffic before  entering the intersection  
> y - denotes a yellow light  
> r - denotes a red light  

```
tl.duration = [20,5,20]
```  
Sets the duration of each state given in the tl.state function.

## Pedestrian Object
The pedestrian object allows the user to create a pedestrian and assign them a path to follow throughout the simulation. The pedestrian attribute examples are as follows:

```
person = Pedestrian at 0 @ 0
```  
Instantiates the object. 

```
person.name = "Bill"
```  
The pedestrian's name must be unique.

```
person.route = ["startRoad", "endRoad"]
```  
The route must have a sidewalk or cross walk for the pedestrian to be able to complete the path.

```
person.departTime = 0
```  
The pedestrian will be delayed until the depart time matches the step in the simulation.

```
person.distance = 0
```  
The pedestrian will be placed 10 units away from the starting node.

```
person.arrivalPos = 10
```  
Sets the pedestrians arrival position.  

## Parking Lot  
The parking lot controls where parking lots are created and the style of the stalls that are available in that parking lot. The parking lot attribute examples are as follows.  

```
parkLot = ParkingLot at 0 @ 0
```  
Instantiates the object. 

```
parkLot.name = "parkingLot"
```  
Sets the name of the parking lot. Must be a unique name.  

```
parkLot.lane = "laneId"
```  
Sets which lane will have parking spots attached to them.  

```
parkLot.startPos = 0
```  
Sets when the parking lot starts on a given lane. The lane must be as long as the difference between the startPos and endPos.  

```
parkLot.endPos = 100
``` 
Sets when the parking lot ends on the given lane. the lane must be as long as the difference between the startPos and endPos.  

```
parkLot.capacity = 5
```  
Sets the amount of parking spots in the parking lot area.  

```
parkLot.angle = 90
```  
Sets the angle of the parking stalls. The parking angle is set to 90 so the car will be facing toward the road for default.

## Random Vehicles  
This object adds random vehicles to the scene with some customizable variables. If this is referenced than a file will be created called trips.trips.xml, this file contains all the trips that will happen in the scene. This file will be overwritten when random vehicles are used in another Sumo map.  

```
randomCars = RandomTrips at 0 @ 0
```  
Instantiates the object.  

```
randomCars.minDistance = 10
```  
Sets the minimum distance that the start edge and end edge must be from each other.  

```
randomCars.maxDistance = 10
```  
Sets the maximum distance that the start edge and end edge can be from each other.  

```
randomCars.spawnPeriod = 10
```  
Sets the amount of time steps between each car spawning. This is set to 15 as a default.  
## Random Car Object  
The random car object allows for specific values to be given random values when the application is run. It extends from a regular Car object so it will have all of the same attributes as the car object. An example of how to create and implement a random car object is below.  

In the scenario file add,  
```
class RandomCar(Car):
    randomDistance: Range(0,1000)
    randomSpeed: Range(0,100)
```
After this, declare a RandomCar. Do not set car.distance or car.speed, they will be overwritten by the random values.
