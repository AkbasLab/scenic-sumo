import os, sys
import scenic
import traci

scenario = scenic.scenarioFromFile("C:\\Users\crump\\OneDrive\\Documents\\GitHub\\Scenic-Sumo\\behindCarWithPedestrian.scenic")

scene = scenario.generate(maxIterations = 1, verbosity = 0, feedback = None)
sumoBinary = 'sumo-gui'
sumoCmd = [sumoBinary, "-c", "Map\\TwoWayJunction\\TwoWayJunction.sumocfg"]

traci.start(sumoCmd)
count = 0
trip = "trip" + count

#Creates all the routes
for x in scene[0].objects:
    traci.route.add(trip, scene[0].objects[x].route)

for x in scene[0].objects:

#Objects get added to the front of the tuple
print(scene[0].objects[1].route)

#Creates the routes for the vehicle to follow
traci.route.add("topTrip", scene[0].objects[1].route)
traci.route.add("bottomTrip", scene[0].objects[0].route)

#Creates the vehicle and assigns the trip to the vehicle
traci.vehicle.add(scene[0].objects[1].name, "topTrip")
traci.vehicle.add(scene[0].objects[0].name, "bottomTrip")

#sets the top actor x units ahead
traci.vehicle.moveTo(scene[0].objects[1].name, 'e1_0', scene[0].objects[1].distance)

#Runs simulation to completion
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulation.step()

traci.close()
