import os, sys
import scenic
import traci




'''Connects to the scenic file and sumo-gui'''
def connectScenicSumo():
    scenario = scenic.scenarioFromFile("C:\\Users\\crump\\OneDrive\\Documents\\GitHub\\Scenic-Sumo\\Scenarios\\FourWayIntersection.scenic")

    scene = scenario.generate(maxIterations = 1, verbosity = 0, feedback = None)
    sumoBinary = 'sumo-gui'
    sumoCmd = [sumoBinary, "-c", "Map\\FourWayIntersection\\FourWayIntersection.sumocfg"]
    traci.start(sumoCmd)

    return scene

'''Creates all of the actors in the simulation'''
def runSimulation():
    count = 0
    step = 0
    trip = "trip" + str(count)
    scene = connectScenicSumo()

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
            print("Not Yet Implemented")

        if str(type(x)) == "<class 'scenic.simulators.sumo.model.Biker>":
            print("Not Yet Implemented")

    phases = []
    phases.append(traci.trafficlight.Phase(20, "GGGgrrrrGGGgrrrr", next=()))
    phases.append(traci.trafficlight.Phase(20, "yyyyrrrryyyyrrrr", next=()))
    phases.append(traci.trafficlight.Phase(20, "rrrrGGGgrrrrGGGg", next=()))

    trafficLightData = traci.trafficlight.Logic("gneJ1", 0, 0, phases)
    traci.trafficlight.setCompleteRedYellowGreenDefinition("gneJ1", trafficLightData)
    print(traci.trafficlight.getCompleteRedYellowGreenDefinition("gneJ1"))

    #traci.trafficlight.setPhase("gneJ1", 3) Changes the state from within the phases
    #print(traci.trafficlight.getRedYellowGreenState("gneJ1"))

    durration = 30

    #Runs simulation to completion
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulation.step()

    traci.close()

if __name__ == '__main__':
    runSimulation()