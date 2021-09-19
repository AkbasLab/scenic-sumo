import scenic
import traci
import argparse
import config
import os
import xml.etree.ElementTree as xml

def getAruments():
    parser = argparse.ArgumentParser(description='Get files for scenic and sumo-gui')
    parser.add_argument('-sc', type = str, help = 'Scenic File name')
    parser.add_argument('-so', type = str, help = 'Sumo File name')
    args = parser.parse_args()
    return args

def connectScenicSumo(args : argparse.Namespace):
    scenario = scenic.scenarioFromFile(os.path.join("Scenarios", args.sc))
    scene = scenario.generate(maxIterations = 1, verbosity = 0, feedback = None)

    checkForParkingLot(scene)

    folderName = args.so.split(".")
    sumoCmd = setSumoParam(folderName)
    
    traci.start(sumoCmd)

    return scene  

def checkForParkingLot(scene):
    for scenicObj in scene[0].objects:
        if str(type(scenicObj)) == "<class 'scenic.simulators.sumo.model.ParkingLot'>":
            createParkingLot(scenicObj)

def createPedestrian(scenicObj):

    traci.person.add(scenicObj.name, scenicObj.route[0], scenicObj.distance, depart = scenicObj.departTime)
    traci.person.appendWalkingStage(scenicObj.name, scenicObj.route, scenicObj.arrivalPos)
    traci.person.setWidth(scenicObj.name, 1)
    traci.person.setLength(scenicObj.name, .5)

def createTrafficLight(scenicObj):

    if type(scenicObj.state) == str and type(scenicObj.duration) == str:
        states = scenicObj.state.split(",")
        duration = scenicObj.duration.split(",")
        phases = []
        for y in range(0, len(states)):
            phases.append(traci.trafficlight.Phase(int(duration[y]), states[y]))

        trafficData = traci.trafficlight.Logic(scenicObj.name, 0 , 0, phases)
        traci.trafficlight.setCompleteRedYellowGreenDefinition(scenicObj.name, trafficData)
    else:
        print("Enter traffic light state and duration as string")

def createRandomCar(road: str, scenicObj):
   
    if scenicObj.randomDistance <= traci.lane.getLength(road[1] + '_' + str(scenicObj.lane)):
        traci.vehicle.moveTo(scenicObj.name, road[1] + '_' + str(scenicObj.lane), scenicObj.randomDistance)
    else:
        print("Scenic Object: randomDistance range is out of bounds of road.")  

    if scenicObj.randomSpeed >= 0:  
        traci.vehicle.setSpeed(scenicObj.name, scenicObj.randomSpeed)  
    else:
        print("Scenic Object: randomSpeed range is out of bounds.")    

def createCar(count : int, scenicObj):
    trip = "trip" + str(count)

    traci.route.add(trip, scenicObj.route)
    traci.vehicle.add(scenicObj.name, trip)

    road = str(scenicObj.route)
    road = road.split("'")

    if str(type(scenicObj)) == "<class '__main__.RandomCar'>":
        createRandomCar(road, scenicObj)

    if scenicObj.track == 1:
        traci.gui.track(scenicObj.name)

    if scenicObj.distance != 0:
        traci.vehicle.moveTo(scenicObj.name, road[1] + '_' + str(scenicObj.lane), scenicObj.distance)

    if scenicObj.xPos != 0 or scenicObj.yPos != 0:
        traci.vehicle.moveToXY(scenicObj.name, road, scenicObj.lane,  scenicObj.xPos, 
                               scenicObj.yPos, angle = scenicObj.angle, keepRoute = scenicObj.vehPlacement)
    
    if scenicObj.speed != -1:
        traci.vehicle.setSpeed(scenicObj.name, scenicObj.speed)

    if scenicObj.speedMode != "":
        traci.vehicle.setSpeedMode(scenicObj.name, scenicObj.speedMode)

    if scenicObj.color != "":
        traci.vehicle.highlight(scenicObj.name, scenicObj.color, size = scenicObj.size)

    if scenicObj.changeSpeed != "":
        traci.vehicle.slowDown(scenicObj.name, scenicObj.changeSpeed[0], scenicObj.changeSpeed[1])
    
    if scenicObj.tau != 0:
        traci.vehicle.setTau(scenicObj.name, scenicObj.tau)
    
    if scenicObj.carParam != 0:
        traci.vehicle.setParameter(scenicObj.name, "junctionModel.ignoreTypes", "DEFAULT_VEHTYPE")
    
    if scenicObj.parkPos != "":
        traci.vehicle.setParkingAreaStop(scenicObj.name, scenicObj.parkPos[0], duration = scenicObj.parkPos[1])

    print(scenicObj.name + " __speed__:" + str(scenicObj.randomSpeed) + "__distance__" + str(scenicObj.randomDistance))
    
def iterateScene(scene : tuple):
    count = 0   
    for scenicObj in scene[0].objects:
        if str(type(scenicObj)) == "<class 'scenic.simulators.sumo.model.Car'>" or \
           str(type(scenicObj)) == "<class '__main__.RandomCar'>":
            createCar(count, scenicObj)
            count += 1

        if str(type(scenicObj)) == "<class 'scenic.simulators.sumo.model.TrafficLight'>":
            createTrafficLight(scenicObj)

        if str(type(scenicObj)) == "<class 'scenic.simulators.sumo.model.Pedestrian'>":
            createPedestrian(scenicObj)

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

def createParkingLot(scenicObj):
    root = xml.Element("additional")

    xml.SubElement(root,"parkingArea", id=scenicObj.name, lane=scenicObj.lane,startPos=str(scenicObj.startPos), 
                endPos=str(scenicObj.endPos),roadsideCapacity=str(scenicObj.capacity),angle=str(scenicObj.angle),
                length="5").text

    xml.SubElement(root, "vType", id="example", 
                maneuverAngleTimes="10 3.0 4.0,80 1.6 11.0,110 11.0 2.0,170 8.1 3.0,181 3.0 4.0")

    tree = xml.ElementTree(root)
    tree.write("parkinglot.net.xml")

if __name__ == '__main__': 
    args = getAruments()
    scene = connectScenicSumo(args)
    iterateScene(scene)
    runSimulation()