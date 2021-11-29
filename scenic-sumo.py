import scenic
import traci
import argparse
import os
import xml.etree.ElementTree as xml
from Utilities.config import SUMO
import Utilities as randomTrips
from traci.constants import LCA_WANTS_LANECHANGE


vehicleList = []

def getAruments() -> argparse.Namespace:
    """Gets the scenic and sumo file from the command line

    Returns:
        argparse.Namespace: The *.scenic file and *.sumocfg file provided by the user
    """
    parser = argparse.ArgumentParser(description='Get files for scenic and sumo-gui')
    parser.add_argument('-sc', type = str, help = 'Scenic File name')
    parser.add_argument('-so', type = str, help = 'Sumo File name')
    args = parser.parse_args()
    return args

def connectScenicSumo(args : argparse.Namespace) -> tuple:
    """Gets scene information from Scenic. Sends information to respective functions. 

    Args:
        args (argparse.Namespace): The scenic file and the sumo config file

    Returns:
        tuple: A tuple of all actors in the scene from Scenic
    """
    scenario = scenic.scenarioFromFile(os.path.join("Scenarios", args.sc))
    scene = scenario.generate(maxIterations = 1, verbosity = 0, feedback = None)

    folderName = args.so.split(".")
    sumoCmd = setSumoParam(folderName)

    checkForUtilities(scene, folderName)

    traci.start(sumoCmd)
    return scene  

def checkForUtilities(scene : tuple, folderName : str):
    """Checks for Utility files that will be used in the scene

    Args:
        scene (tuple): A list of the actors in the Scenic scene.

        folderName (str): A string containing the Map folder.
    """
    for scenicObj in scene[0].objects:
        if str(type(scenicObj)) == "<class 'scenic.simulators.sumo.model.ParkingLot'>":
            createParkingLot(scenicObj)
        
        if str(type(scenicObj)) == "<class '__main__.RandomTrips'>":
            createRandomTrips(scenicObj, folderName)

def createPedestrian(scenicObj):
    """Iterates through scenic object to create a pedestrian.

    Args:
        scenicObj (model.Pedestrian): An object containing information to create a 
        pedestrian
    """
    traci.person.add(scenicObj.name, scenicObj.route[0], scenicObj.distance, depart = scenicObj.departTime)
    traci.person.appendWalkingStage(scenicObj.name, scenicObj.route, scenicObj.arrivalPos)
    traci.person.setWidth(scenicObj.name, 1)
    traci.person.setLength(scenicObj.name, .5)

def createTrafficLight(scenicObj):
    """Creates a traffic light from the scenic object

    Args:
        scenicObj (model.TrafficLight): An object containing information to change the
        state of a traffic light
    """
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
    """Creates a car with random attributes from the scenic object

    Args:
        road (str): Is the edge which the car is on
        scenicObj (___main___.RandomCar): An object containing information to create 
        a car with random values
    """
    print(str(scenicObj.randomDistance) + " " + str(scenicObj.randomSpeed))
    if scenicObj.randomDistance <= traci.lane.getLength(road[1] + '_' + str(scenicObj.lane)) and \
        scenicObj.randomDistance != 0:
        traci.vehicle.moveTo(scenicObj.name, road[1] + '_' + str(scenicObj.lane), scenicObj.randomDistance)
    else:
        print("Scenic Object: randomDistance range is out of bounds of road.")  

    if scenicObj.randomSpeed >= 0:  
        traci.vehicle.setSpeed(scenicObj.name, scenicObj.randomSpeed)  
    else:
        print("Scenic Object: randomSpeed range is out of bounds.")    

def createCar(carCount : int, scenicObj):
    """Creates a car from the scenic object

    Args:
        count (int): The number of cars in the simulation. Insures a unique car ID

        scenicObj (model.Car): An object containing information to create a car
    """
    trip = "trip" + str(carCount)

    if scenicObj.route != "" and scenicObj.name != "":
        traci.route.add(trip, scenicObj.route)
        traci.vehicle.add(scenicObj.name, trip)
    else:
        print("The name and route must be filled when creating a vechicle.")
    
    road = str(scenicObj.route)
    road = road.split("'")

    if str(type(scenicObj)) == "<class '__main__.RandomCar'>":
        createRandomCar(road, scenicObj)

    if scenicObj.track == 1:
        traci.gui.track(scenicObj.name)

    if scenicObj.distance != 0 or \
        scenicObj.distance > traci.lane.getLength(road[1] + '_' + str(scenicObj.lane)):
        traci.vehicle.moveTo(scenicObj.name, road[1] + '_' + str(scenicObj.lane), scenicObj.distance)

    if scenicObj.xPos != 0 or scenicObj.yPos != 0:
        traci.vehicle.moveToXY(scenicObj.name, road, scenicObj.lane,  scenicObj.xPos, 
                               scenicObj.yPos, angle = scenicObj.angle, keepRoute = scenicObj.vehPlacement)
    
    if scenicObj.speed != -1:
        traci.vehicle.setSpeed(scenicObj.name, scenicObj.speed)

    if scenicObj.lane != 0:
        traci.vehicle.changeLane(scenicObj.name, scenicObj.lane, 15)

    if scenicObj.speedMode != "":
        traci.vehicle.setSpeedMode(scenicObj.name, scenicObj.speedMode)

    if scenicObj.color != "":
        traci.vehicle.setColor(scenicObj.name, scenicObj.color)

    if scenicObj.changeSpeed != "" and scenicObj.changeSpeed[2] == 0:
        traci.vehicle.slowDown(scenicObj.name, scenicObj.changeSpeed[0], scenicObj.changeSpeed[1])
    
    if scenicObj.tau != 0:
        traci.vehicle.setTau(scenicObj.name, scenicObj.tau)
    
    if scenicObj.carParam != 0:
        traci.vehicle.setParameter(scenicObj.name, "junctionModel.ignoreTypes", "DEFAULT_VEHTYPE")
    
    if scenicObj.parkPos != "":
        traci.vehicle.setParkingAreaStop(scenicObj.name, scenicObj.parkPos[0], duration = scenicObj.parkPos[1])
    
    if scenicObj.laneMode != 0:
        traci.vehicle.setLaneChangeMode(scenicObj.name, scenicObj.laneMode)

def iterateScene(scene : tuple):
    """Iterates through the Scenic scene and calls the correct function to create the 
    actors

    Args:
        scene (tuple): A list of all the actors in the Scenic scene
    """
    count = 0   
    for scenicObj in scene[0].objects:

        if str(type(scenicObj)) == "<class 'scenic.simulators.sumo.model.Car'>" or \
           str(type(scenicObj)) == "<class '__main__.RandomCar'>":
            createCar(count, scenicObj)
            vehicleList.append(scenicObj)
            count += 1

        if str(type(scenicObj)) == "<class 'scenic.simulators.sumo.model.TrafficLight'>":
            createTrafficLight(scenicObj)

        if str(type(scenicObj)) == "<class 'scenic.simulators.sumo.model.Pedestrian'>":
                createPedestrian(scenicObj)

def runSimulation():
    """
    Runs the simulation to completion
    """

    while traci.simulation.getMinExpectedNumber() > 0:
        for scenicObj in vehicleList:
            if scenicObj.laneChanges != "" and \
               scenicObj.laneChanges[1] == traci.simulation.getTime():
                traci.vehicle.changeLane(scenicObj.name, scenicObj.laneChanges[0], 50)
            if scenicObj.changeSpeed != "" and \
                scenicObj.changeSpeed[2] == traci.simulation.getTime():
                 traci.vehicle.slowDown(scenicObj.name, scenicObj.changeSpeed[0], scenicObj.changeSpeed[1])
        traci.simulation.step()
    traci.close()

def setSumoParam(folderName : str) -> list:
    """Gets the SUMO configuration settings from the Utilities/config.py file and 
    adds them to the terminal command at runtime

    Args:
        folderName (str): The SUMO file name

    Returns:
        list: A list of optional commands for SUMO
    """
    
    sim = SUMO
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
    """Creates a parking lot using the scenic object

    Args:
        scenicObj (model.ParkingLot): An object containing information to create a parking
        lot on an edge
    """
    root = xml.Element("additional")

    xml.SubElement(root,"parkingArea", id=scenicObj.name, lane=scenicObj.lane,startPos=str(scenicObj.startPos), 
                endPos=str(scenicObj.endPos),roadsideCapacity=str(scenicObj.capacity),angle=str(scenicObj.angle),
                length="5").text

    xml.SubElement(root, "vType", id="example", 
                maneuverAngleTimes="10 3.0 4.0,80 1.6 11.0,110 11.0 2.0,170 8.1 3.0,181 3.0 4.0")

    tree = xml.ElementTree(root)
    tree.write(os.path.join("Utilities", "parkinglot.net.xml"))

def createRandomTrips(scenicObj, folderName : str):
    """Creates random trips using the randomTrips.py file

    Args:
        scenicObj (__main__.RandomTrips): An object containing the information to 
        create random trips for vehicles.

        foldername (str): A string containing the folder name of the file being run.
    """
    
    args = []
    args.append("-n")
    args.append(os.path.join(os.getcwd(),"Map", folderName[0], folderName[0] + ".net.xml"))

    if scenicObj.minDistance != 0:
        args.append("--min-distance")
        args.append(str(scenicObj.minDistance))

    if scenicObj.maxDistance != 0:
        args.append("--max-distance")
        args.append(str(scenicObj.maxDistance))

    if scenicObj.spawnPeriod != 0:
        args.append("-p")
        args.append(str(scenicObj.spawnPeriod))

    args.append("-r")
    args.append(os.path.join(os.getcwd(), "Map", folderName[0], "trips.trips.xml"))
    
    options = randomTrips.get_options(args)
    #randomTrips.main(options)

if __name__ == '__main__': 
    args = getAruments()
    scene = connectScenicSumo(args)
    iterateScene(scene)
    runSimulation()