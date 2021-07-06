import os, sys
import scenic
import traci

scenario = scenic.scenarioFromFile("C:\\Users\crump\\OneDrive\\Documents\\GitHub\\Scenic-Sumo\\behindCarWithPedestrian.scenic")

scene = scenario.generate(maxIterations = 1, verbosity = 0, feedback = None)
sumoBinary = 'sumo-gui'
sumoCmd = [sumoBinary, "-c", "Map\\TwoWayJunction\\TwoWayJunction.sumocfg"]

traci.start(sumoCmd)
count = 0
trip = "trip" + str(count)

#Creates all the routes
for x in scene[0].objects:
    trip = "trip" + str(count)
    traci.route.add(trip, x.route)
    count += 1

count = 0
#Creates all vehicles and places them on routes
for x in scene[0].objects:
    trip = "trip" + str(count)
    traci.vehicle.add(x.name, trip)
    count += 1

#sets the top actor x units ahead
traci.vehicle.moveTo(scene[0].objects[1].name, 'e1_0', scene[0].objects[1].distance)

#Runs simulation to completion
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulation.step()

traci.close()
