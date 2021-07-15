import os, sys
import scenic
import traci

def connectScenicSumo():
    scenario = scenic.scenarioFromFile("C:\\Users\\crump\\OneDrive\\Documents\\GitHub\\Scenic-Sumo\\Scenarios\\FourWayIntersection.scenic")

    scene = scenario.generate(maxIterations = 1, verbosity = 0, feedback = None)
    sumoBinary = 'sumo-gui'
    sumoCmd = [sumoBinary, "-c", "Map\\FourWayIntersection\\FourWayIntersection.sumocfg"]
    traci.start(sumoCmd)

    return scene

def createTrafficLight(x):
    states = str(x.state)
    states = states.split(",")
    
    duration = str(x.duration)
    duration = duration.split(",")

    phases = []
    for y in range(0, len(states)):
        print(duration[y])
        phases.append(traci.trafficlight.Phase(int(duration[y]), states[y]))
    
    trafficData = traci.trafficlight.Logic(x.name, 0 , 0, phases)
    traci.trafficlight.setCompleteRedYellowGreenDefinition(x.name, trafficData)

def createCar(count, x):
    trip = "trip" + str(count)
    traci.route.add(trip, x.route)
        
    traci.vehicle.add(x.name, trip)
         
    if x.distance != 0:
        road = str(x.route)
        road = road.split("'")
        traci.vehicle.moveTo(x.name, road[1] + '_' + str(x.lane), x.distance)

def iterateScene():
    count = 0   
    scene = connectScenicSumo()

    for x in scene[0].objects:
        print(type(x))
        if str(type(x)) == "<class 'scenic.simulators.sumo.model.Car'>":
            createCar(count, x)
            count += 1
   
        if str(type(x)) == "<class 'scenic.simulators.sumo.model.Pedestrian'>":
            print("Not Yet Implemented")

        if str(type(x)) == "<class 'scenic.simulators.sumo.model.Biker>":
            print("Not Yet Implemented")

        if str(type(x)) == "<class 'scenic.simulators.sumo.model.TrafficLight'>":
            createTrafficLight(x)

def runSimulation():
    #Runs simulation to completion
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulation.step()

    traci.close()

if __name__ == '__main__':
    runSimulation()