''''
Luke Crump 1/2/2022
@crumpl07
'''

try:
    import traci
except ImportError as e:
    raise ModuleNotFoundError('Sumo scenes require the "traci" Python package') from e

import scenic
import os
import xml.etree.ElementTree as xml
from scenic.simulators.sumo.Utilities.config import SUMO
import scenic.simulators.sumo.Utilities.randomTrips as randomTrips
from scenic.core.scenarios import Scene

import numpy as np

def euclidean_distance(p0 : list, p1 : list) -> float:
    return np.sqrt((p0[0]-p1[0])**2 + (p0[1]-p1[1])**2)

class SumoSimulator:
    
    def __init__(self, map_file : str, scenic_file : str, sumo_config : dict):
        """Sets up the simulator to run scenic simulations

        Args: 
            map_file (str): A *.sumocfg map file.
            scenic_file (str): A *.scenic file.
        """
        self.map_File = map_file
        self.scenic_file = scenic_file
        self.scenario_number = 0
        self.sumo_config = sumo_config

        self._scenes = []
        self._sims = []
        self.createSimulation()

    def createSimulation(self):
        self.scenario_number += 1
        sim = SumoSimulation(
            self.scenario_number, 
            self.map_File, 
            self.scenic_file, 
            self.sumo_config
        )
        self._sims.append(sim)
        self._scenes.append(sim.scene)
        return sim

    @property
    def scenes(self):
        return self._scenes

    @property
    def sims(self):
        return self._sims

class SumoSimulation:
    
    

    def __init__(self, scenario_number : int, map_file : str, scenic_file : str, sumo_config : dict):
        """Sets up an individual scenic simulation.

        Args:
            scene (tuple): A tuple containing all the actors in the scene and their information.
            scenario_number (int): The number of the current scene.
            map_file (str): A *.sumocfg map file.
            scenic_file (str): A *.scenic scene file.
            sumo_config (dict): A list of commands to control SUMO interface.
        """
        self.scenario_number = scenario_number
        self.map_file = map_file
        self.scenic_file = scenic_file

        self.__vehicle_list = []
        self.__pedestrian_list = []
        self.__ped_ego_wait_at_xing_event = []

        self._scenario = scenic.scenarioFromFile(scenic_file)
        self._scene = self._scenario.generate(maxIterations = 2, verbosity = 0, feedback = 0)

        self._sumo_config = sumo_config
        sumo_cmd = self.__setSumoParam(self.map_file, sumo_config)
        self.__checkForUtilities(self._scene, self.map_file)
        traci.start(sumo_cmd)        

        if self._sumo_config["gui"]:
            traci.gui.setSchema(traci.gui.DEFAULT_VIEW, "real world")

        self.__iterateScene(self._scene)
        self.__runSimulation()

    @property
    def scene(self) -> Scene:
        return self._scene[0]

    @property
    def ped_ego_wait_at_xing_event(self) -> list:
        return self.__ped_ego_wait_at_xing_event


    def __checkForUtilities(self, scene : tuple, folderName : str):
        """Checks for Utility files that will be used in the scene.

        Args:
            scene (tuple): A list of the actors in the Scenic scene.

            folderName (str): A string containing the Map folder.
        """
        for scenicObj in scene[0].objects:
            if str(type(scenicObj)) == "<class 'scenic.simulators.sumo.model.ParkingLot'>":
                self.__createParkingLot(scenicObj)
            
            if str(type(scenicObj)) == "<class 'scenic.simulators.sumo.model.RandomTrips'>":
                self.__createRandomTrips(scenicObj, folderName)
                
    def __createRandomTrips(self, scenicObj, folder_name : str):
        """Creates random trips using the randomTrips.py file.

        Args:
            scenicObj (__main__.RandomTrips): An object containing the information to 
            create random trips for vehicles.

            foldername (str): A string containing the folder name of the file being run.
        """
        args = []
        args.append("-n")
        map_name = os.path.basename(folder_name)
        file = map_name.split(".")
        
        args.append(os.path.join(os.path.dirname(folder_name), file[0] + ".net.xml"))

        if scenicObj.minDistance != 0:
            args.append("--min-distance")
            args.append(str(scenicObj.minDistance))

        if scenicObj.maxDistance != 0:
            args.append("--max-distance")
            args.append(str(scenicObj.maxDistance))
 
        if scenicObj.spawnPeriod != 15:
            args.append("-p")
            args.append(str(scenicObj.spawnPeriod))
        
        options = randomTrips.get_options(args)
        randomTrips.main(options)

    def __createParkingLot(self, scenicObj):
        """Creates a parking lot using the scenic object.

        Args:
            scenicObj (model.ParkingLot): An object containing information to create a parking
            lot on an edge.
        """
        root = xml.Element("additional")

        xml.SubElement(root,"parkingArea", id=scenicObj.name, lane=scenicObj.lane,startPos=str(scenicObj.startPos), 
                    endPos=str(scenicObj.endPos),roadsideCapacity=str(scenicObj.capacity),angle=str(scenicObj.angle),
                    length="5").text

        xml.SubElement(root, "vType", id="example", 
                    maneuverAngleTimes="10 3.0 4.0,80 1.6 11.0,110 11.0 2.0,170 8.1 3.0,181 3.0 4.0")

        tree = xml.ElementTree(root)
        tree.write(os.path.join("Utilities", "parkinglot.net.xml"))

    def __setSumoParam(self, file_name : str, sumo_config : dict) -> list:
        """Gets the SUMO configuration settings from the Utilities/config.py file and 
        adds them to the terminal command at runtime

        Args:
            file_name (str): The SUMO file name.
            sumo_config (dict): A list of commands to control the SUMO interface.

        Returns:
            list: A list of optional commands for SUMO.
        """
        cmd = []
        for key, val in sumo_config.items():
            
            if key == "gui":
                if val == True:
                    cmd.append("sumo-gui")
                    cmd.append("-n")
                    cmd.append(file_name)
                else:
                    cmd.append("sumo")
                    cmd.append("-n")
                    cmd.append(file_name)
            else:
                cmd.append(key)
                if (val == "") or (val == None) or (val == True):
                    pass
                else:
                    cmd.append(str(val))
        return cmd    

    def __iterateScene(self, scene : tuple):
        """Iterates through the scene to add all the actors.

        Args:
            scene (tuple): A list of all the actors in the Scenic scene
        """
        count = 0   
        for scenicObj in scene[0].objects:
        
            if str(type(scenicObj)) == "<class 'scenic.simulators.sumo.model.Car'>" or \
            str(type(scenicObj)) == "<class '__main__.RandomCar'>":
                self.__createCar(count, scenicObj)
                self.__vehicle_list.append(scenicObj)
                count += 1

            if str(type(scenicObj)) == "<class 'scenic.simulators.sumo.model.TrafficLight'>":
                self.__createTrafficLight(scenicObj)

            if str(type(scenicObj)) == "<class 'scenic.simulators.sumo.model.Pedestrian'>":
                self.__createPedestrian(scenicObj)
                self.__pedestrian_list.append(scenicObj)
                self.__ped_ego_wait_at_xing_event.append(-1)
        return

    def __createCar(self, carCount : int, scenicObj):
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
            print("The name and route must be filled when creating a vehicle.")
        
        road = str(scenicObj.route)
        road = road.split("'")

        if str(type(scenicObj)) == "<class '__main__.RandomCar'>":
            self.__createRandomCar(road, scenicObj)

        if scenicObj.track == 1:
            if self._sumo_config["gui"]:
                traci.gui.track(scenicObj.name)
                traci.gui.setZoom(traci.gui.DEFAULT_VIEW, 400)

        if scenicObj.distance != 0 or \
            scenicObj.distance > traci.lane.getLength(road[1] \
                + '_' + str(scenicObj.lane)):
            traci.vehicle.moveTo(scenicObj.name, road[1] \
                + '_' + str(scenicObj.lane), scenicObj.distance)

        if scenicObj.xPos != 0 or scenicObj.yPos != 0:
            traci.vehicle.moveToXY(scenicObj.name, road, scenicObj.lane,  scenicObj.xPos, 
                                scenicObj.yPos, angle = scenicObj.angle, keepRoute = scenicObj.vehPlacement)
        
        if scenicObj.speed != -1:
            traci.vehicle.setMaxSpeed(scenicObj.name, scenicObj.speed)
            traci.vehicle.setSpeed(scenicObj.name, scenicObj.speed)

        if scenicObj.lane != 0:
            traci.vehicle.changeLane(scenicObj.name, scenicObj.lane, 3)

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

    def __createRandomCar(self, road: str, scenicObj):

        """Creates a car with random attributes from the scenic object

        Args:
            road (str): Is the edge which the car is on
            scenicObj (___main___.RandomCar): An object containing information to create 
            a car with random values
        """
        if scenicObj.randomDistance <= traci.lane.getLength(road[1] + '_' + str(scenicObj.lane)) and \
            scenicObj.randomDistance != 0:
            traci.vehicle.moveTo(scenicObj.name, road[1] + '_' + str(scenicObj.lane), scenicObj.randomDistance)
        else:
            print("Scenic Object: randomDistance range is out of bounds of road.")  

        if scenicObj.randomSpeed >= 0:  
            traci.vehicle.setSpeed(scenicObj.name, scenicObj.randomSpeed)  
        else:
            print("Scenic Object: randomSpeed range is out of bounds.")

    def __createTrafficLight(self, scenicObj):
        """Creates a traffic light from the scenic object

        Args:
            scenicObj (model.TrafficLight): An object containing information to change the
            state of a traffic light
        """
        if (len(scenicObj.state) > 0) and (len(scenicObj.duration) > 0):
            assert len(scenicObj.state) == len(scenicObj.duration)
            states = scenicObj.state
            duration = scenicObj.duration
            phases = []
            for y in range(0, len(states)):
                phases.append(traci.trafficlight.Phase(
                    float(duration[y]), states[y]))
            trafficData = traci.trafficlight.Logic(
                scenicObj.name, 0 , 0, phases)
            traci.trafficlight.setCompleteRedYellowGreenDefinition(
                scenicObj.name, trafficData)
        return


    def __createPedestrian(self, scenicObj):

        """Creates a pedestrian.

        Args:
            scenicObj (model.Pedestrian): An object containing information to create a 
            pedestrian
        """
        traci.person.add(scenicObj.name, scenicObj.route[0], scenicObj.distance, depart = scenicObj.departTime)
        traci.person.appendWalkingStage(scenicObj.name, scenicObj.route, scenicObj.arrivalPos)
        traci.person.setWidth(scenicObj.name, 1)
        traci.person.setLength(scenicObj.name, .5)
        traci.person.setColor(scenicObj.name, scenicObj.color)


    

    def __runSimulation(self):
        """
        Runs the simulation to completion
        """
        
        while traci.simulation.getMinExpectedNumber() > 0:
            
            # Pedestrian
            for i, pedObj in enumerate(self.__pedestrian_list):
                # Pedestrian is in the sim
                if pedObj.egoWaitAtXing \
                    and (pedObj.name in traci.person.getIDList()) \
                    and ("_c" in traci.person.getRoadID(pedObj.name)) \
                    and (traci.vehicle.getSpeed("ego") == 0) \
                    and (euclidean_distance(
                        traci.person.getPosition(pedObj.name),
                        traci.vehicle.getPosition("ego")
                    ) < 10):
                    self.__ped_ego_wait_at_xing_event[i] = \
                        traci.simulation.getTime()
                continue    

            # Vehicle Lane Change
            for scenicObj in self.__vehicle_list:
                if scenicObj.laneChanges != "" and \
                scenicObj.laneChanges[1] == traci.simulation.getTime():
                    traci.vehicle.changeLane(scenicObj.name, scenicObj.laneChanges[0], 3)

                if scenicObj.changeSpeed != "" and \
                    scenicObj.changeSpeed[2] == traci.simulation.getTime():
                    traci.vehicle.slowDown(scenicObj.name, scenicObj.changeSpeed[0], scenicObj.changeSpeed[1])

            # End the sim if the ego doesn't exist
            if not "ego" in traci.vehicle.getIDList():
                break

            traci.simulation.step()

        traci.close()