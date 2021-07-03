import traci

sumoBinary = 'sumo-gui'
sumoCmd = [sumoBinary, "-c", "Map\\TwoWayJunction\\TwoWayJunction.sumocfg"]

traci.start(sumoCmd)

#Creates the routes for the vehicle to follow
traci.route.add("topTrip", ["e1", "e3"])
traci.route.add("bottomTrip", ["e2", "e3"])

#Creates the vehicle and assigns the trip to the vehicle
traci.vehicle.add("vehicle1", "topTrip")
traci.vehicle.add("vehicle2", "bottomTrip")

#sets the top actor x units ahead
traci.vehicle.moveTo("vehicle1", 'e1_0', 50)

#Runs simulation to completion
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulation.step()

traci.close()