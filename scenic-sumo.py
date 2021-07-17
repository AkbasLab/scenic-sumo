import os, sys
import scenic
import traci
import argparse

def getAruments():
    parser = argparse.ArgumentParser(description='Get files for scenic and sumo-gui')
    parser.add_argument('-sc', type = str, help = 'Scenic File name')
    parser.add_argument('-so', type = str, help = 'Sumo File name')
    args = parser.parse_args()
    return args

def connectScenicSumo(args):
    scenario = scenic.scenarioFromFile("C:\\Users\\crump\\OneDrive\\Documents\\GitHub\\Scenic-Sumo\\Scenarios\\" + args.sc)

    scene = scenario.generate(maxIterations = 1, verbosity = 0, feedback = None)
    sumoBinary = 'sumo-gui'
    folderName = args.so.split(".")
    sumoCmd = [sumoBinary, "-c", "Map\\" + folderName[0] + "\\" + args.so]
    traci.start(sumoCmd)

    return scene  

def createPedestrian(x):
    print("hello there")

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

def iterateScene(scene):
    count = 0   

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

        if str(type(x)) == "<class 'scenic.simulators.sumo.model.Pedestrian'>":
            createPedestrian(x)

def runSimulation():
    #Runs simulation to completion
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulation.step()

    traci.close()

if __name__ == '__main__':
    args = getAruments()
    scene = connectScenicSumo(args)
    iterateScene(scene)
    runSimulation()