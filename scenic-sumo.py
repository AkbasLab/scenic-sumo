import os, sys
import scenic
import traci

scenario = scenic.scenarioFromFile("C:\\Users\\crump\\OneDrive\\Documents\\GitHub\\Scenic-Sumo\\behindCarWithPedestrian.scenic")

scene = scenario.generate(maxIterations = 1, verbosity = 0, feedback = None)
sumoBinary = 'sumo-gui'
sumoCmd = [sumoBinary, "-c", "Map\\TwoWayJunction\\TwoWayJunction.sumocfg"]

traci.start(sumoCmd)
count = 0
trip = "trip" + str(count)

for x in scene[0].objects:

    if str(type(x)) == "<class 'scenic.simulators.sumo.model.Car'>":

        #Create routes
        trip = "trip" + str(count)
        traci.route.add(trip, x.route)
        
        #Create vehicles
        traci.vehicle.add(x.name, trip)
        
        #Set Distance 
        if x.distance != 0:
            road = str(x.route)
            road = road.split("'")
            traci.vehicle.moveTo(x.name, road[1] + '_' + str(x.lane), x.distance)
        count += 1    

    if str(type(x)) == "<class 'scenic.simulators.sumo.model.Pedestrian'>":
        print("PEDESTRIAN NOT CURRENTLY SUPPORTED!")

    if str(type(x)) == "<class 'scenic.simulators.sumo.model.Biker>":
        print("BIKER NOT CURRENTLY SUPPORTED!")

#Runs simulation to completion
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulation.step()

traci.close()
