import scenic
import traci
import argparse
import config
import os

def getAruments():
    parser = argparse.ArgumentParser(description='Get files for scenic and sumo-gui')
    parser.add_argument('-sc', type = str, help = 'Scenic File name')
    parser.add_argument('-so', type = str, help = 'Sumo File name')
    args = parser.parse_args()
    return args

def connectScenicSumo(args : argparse.Namespace):
    scenario = scenic.scenarioFromFile(os.path.join("Scenarios", args.sc))
    scene = scenario.generate(maxIterations = 1, verbosity = 0, feedback = None)
    
    folderName = args.so.split(".")
    sumoCmd = setSumoParam(folderName)
    
    traci.start(sumoCmd)

    return scene  

def createPedestrian(x):

    traci.person.add(x.name, x.route[0], x.distance, depart = x.departTime)
    traci.person.appendWalkingStage(x.name, x.route, x.arrivalPos)
    traci.person.setWidth(x.name, 1)
    traci.person.setLength(x.name, .5)

def createTrafficLight(x):
    states = x.state.split(",")
    duration = x.duration.split(",")

    phases = []
    for y in range(0, len(states)):
        phases.append(traci.trafficlight.Phase(int(duration[y]), states[y]))

    trafficData = traci.trafficlight.Logic(x.name, 0 , 0, phases)
    traci.trafficlight.setCompleteRedYellowGreenDefinition(x.name, trafficData)

def createCar(count : int, x):
    trip = "trip" + str(count)

    traci.route.add(trip, x.route)
    traci.vehicle.add(x.name, trip)

    road = str(x.route)
    road = road.split("'")

    if x.track == 1:
        traci.gui.track(x.name)

    if x.distance != 0:
        traci.vehicle.moveTo(x.name, road[1] + '_' + str(x.lane), x.distance)

    if x.xPos != 0 or x.yPos != 0:
        traci.vehicle.moveToXY(x.name, road, x.lane,  x.xPos, x.yPos, angle = x.angle, keepRoute = x.vehPlacement)
    
    if x.speed != -1:
        traci.vehicle.setSpeed(x.name, x.speed)

    if x.speedMode != "":
        traci.vehicle.setSpeedMode(x.name, x.speedMode)

    if x.color != "":
        traci.vehicle.highlight(x.name, x.color, size = x.size)

    if x.changeSpeed != "":
        traci.vehicle.slowDown(x.name, x.changeSpeed[0], x.changeSpeed[1])
    
    if x.tau != 0:
        traci.vehicle.setTau(x.name, x.tau)
    
    if x.carParam != 0:
        traci.vehicle.setParameter(x.name, "junctionModel.ignoreTypes", "DEFAULT_VEHTYPE")

def iterateScene(scene : tuple):
    count = 0   
    for x in scene[0].objects:
        if str(type(x)) == "<class 'scenic.simulators.sumo.model.Car'>":
            createCar(count, x)
            count += 1

        if str(type(x)) == "<class 'scenic.simulators.sumo.model.Biker>":
            print("Not Yet Implemented")

        if str(type(x)) == "<class 'scenic.simulators.sumo.model.TrafficLight'>":
            createTrafficLight(x)

        if str(type(x)) == "<class 'scenic.simulators.sumo.model.Pedestrian'>":
            createPedestrian(x)
            
def runSimulation():
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulation.step()

    traci.close()

def setSumoParam(folderName : str):
    sim = config.SUMO
    cmd = []
    for key, val in sim.items():
        
        if key == "gui":
            if val == True:
                cmd.append("sumo-gui")
                cmd.append("-c")
                cmd.append(os.path.join("Map", folderName[0], args.so))
            else:
                cmd.append("sumo")
                cmd.append("-c")
                cmd.append(os.path.join("Map", folderName[0], args.so))
        else:
            cmd.append(key)
            cmd.append(str(val))
    return cmd

if __name__ == '__main__':
    args = getAruments()
    scene = connectScenicSumo(args)
    iterateScene(scene)
    runSimulation()