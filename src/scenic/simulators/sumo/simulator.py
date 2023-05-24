''''
Luke Crump 1/2/2022
@crumpl07
'''

try:
    import traci
    import traci.constants as tc
except ImportError as e:
    raise ModuleNotFoundError('Sumo scenes require the "traci" Python package') from e

import scenic
import os
import xml.etree.ElementTree as xml


from scenic.simulators.sumo.Utilities.config import SUMO
import scenic.simulators.sumo.Utilities.randomTrips as randomTrips
from scenic.core.scenarios import Scene


import numpy as np
# import pandas as pd

def euclidean_distance(p0 : list, p1 : list) -> float:
    return np.sqrt((p0[0]-p1[0])**2 + (p0[1]-p1[1])**2)


class TraCIClient:
    def __init__(self, config : dict, priority : int = 1):
        """
        Barebones TraCI client.

        --- Parameters ---
        priority : int
            Priority of clients. MUST BE UNIQUE
        config : dict
            SUMO arguments stored as a python dictionary.
        """
        
        self._config = config
        self._priority = priority
        

        self.connect()
        return

    @property
    def priority(self) -> int:
        """
        Priority of TraCI client.
        """
        return self._priority

    @property
    def config(self) -> dict:
        """
        SUMO arguments stored as a python dictionary.
        """
        return self._config

    def run_to_end(self):
        """
        Runs the client until the end.
        """
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
            # more traci commands
        return

    def close(self):
        """
        Closes the client.
        """
        traci.close()
        return


    def connect(self):
        """
        Start or initialize the TraCI connection.
        """        
        # Start the traci server with the first client
        if self.priority == 1:
            cmd = []

            for key, val in self.config.items():
                if key == "gui":
                    sumo = "sumo"
                    if val: sumo +="-gui"
                    cmd.append(sumo)
                    continue
                
                if key == "--remote-port":
                    continue

                cmd.append(key)
                if val != "":
                    cmd.append(str(val))
                continue

            traci.start(cmd,port=self.config["--remote-port"])
            traci.setOrder(self.priority)
            return
        
        # Initialize every client after the first.
        traci.init(port=self.config["--remote-port"])
        traci.setOrder(self.priority)
        return


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
        self.sumo_config["--net-file"] = map_file

        self._scenes = []
        self._sims = []

        TraCIClient(self.sumo_config)

        if self.sumo_config["gui"]:
            traci.gui.setSchema(traci.gui.DEFAULT_VIEW, "real world")

        self.init_state_fn = "%s/init-state.xml" % os.path.dirname(map_file)
        traci.simulation.saveState(self.init_state_fn)

        # self.createSimulation()
        return

    def createSimulation(self):
        traci.simulation.loadState(self.init_state_fn)
        self.scenario_number += 1
        sim = SumoSimulation(
            self.scenario_number, 
            # self.map_File, 
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


    def __init__(self, scenario_number : int, scenic_file : str, sumo_config : dict):
        """Sets up an individual scenic simulation.

        Args:
            scene (tuple): A tuple containing all the actors in the scene and their information.
            scenario_number (int): The number of the current scene.
            map_file (str): A *.sumocfg map file.
            scenic_file (str): A *.scenic scene file.
            sumo_config (dict): A list of commands to control SUMO interface.
        """
        self.scenario_number = scenario_number
        # self.map_file = map_file
        self.scenic_file = scenic_file

        self.__vehicle_list = []
        self.__pedestrian_list = []
        self.__ped_ego_wait_at_xing_event = []

        self._scenario = scenic.scenarioFromFile(scenic_file)
        self._scene = self._scenario.generate(maxIterations = 2, verbosity = 0, feedback = 0)

        self._sumo_config = sumo_config
        # sumo_cmd = self.__setSumoParam(self.map_file, sumo_config)
        # self.__checkForUtilities(self._scene, self.map_file)
        # traci.start(sumo_cmd)        

        # if self._sumo_config["gui"]:
        #     traci.gui.setSchema(traci.gui.DEFAULT_VIEW, "real world")

        self.__iterateScene(self._scene)


        # Subscriptions for scoring
        self.__init_scores()
        self.__init_subscriptions()

        self.__runSimulation()

        self._scores_data["ped_ego_wait_at_xing_event"] = self.ped_ego_wait_at_xing_event
        self._score = self._scores_data
        return

    @property
    def scene(self) -> Scene:
        return self._scene[0]

    @property
    def ped_ego_wait_at_xing_event(self) -> list:
        return self.__ped_ego_wait_at_xing_event
    
    @property
    def score(self) -> dict:
        return self._score

    def __init_scores(self):
        self._scores_data = {
            "e_brake_partial" : 0.,
            "e_brake_full" : 0.,
            "e_stop" : 0.,
            "collision" : 0.
        }
        return

    def __init_subscriptions(self):
        traci.vehicle.subscribe("ego", 
            [tc.VAR_SPEED, tc.VAR_DECEL, tc.VAR_EMERGENCY_DECEL])
        traci.simulation.subscribe([tc.VAR_TIME])

        self._sub_data = {
            "timestamp" : [],
            "ego_speed" : [], 
            "ego_decel" : [],
            "ego_e_decel" : []
        }
        return

    def __update_subscriptions_history(self):
        timestamp = traci.simulation.getSubscriptionResults() \
            [tc.VAR_TIME]

        sub = traci.vehicle.getSubscriptionResults("ego")
        ego_speed = sub[tc.VAR_SPEED]
        ego_decel = sub[tc.VAR_DECEL]
        ego_e_decel = sub[tc.VAR_EMERGENCY_DECEL]


        # Add the newest subscriptions to the subscription history
        self._sub_data["timestamp"].append(timestamp)
        self._sub_data["ego_speed"].append(ego_speed)
        self._sub_data["ego_decel"].append(ego_decel)
        self._sub_data["ego_e_decel"].append(ego_e_decel)
        return


    def __score_update(self):
        if len(self._sub_data["timestamp"]) < 2:
            return

        # Deceleration rate
        t0, t1 = self._sub_data["timestamp"][-2:]
        s0, s1 = self._sub_data["ego_speed"][-2:]
        decel = self._sub_data["ego_decel"][-1]
        
        accel = (s1-s0)/(t1-t0)
        accel = np.round(accel, 5)

        # emergency braking
        if accel < -decel:
            e_decel = self._sub_data["ego_e_decel"][-1]
            e_brake_score = ((-accel - decel) / e_decel) * 2

            # print(e_brake_score)

            if e_brake_score == 1:
                self._scores_data["e_brake_full"] = 1.

            elif (e_brake_score < 1) \
                and (e_brake_score > self._scores_data["e_brake_partial"]):
                self._scores_data["e_brake_partial"] = e_brake_score
            
            # Emergency Stop
            elif accel < -e_decel:
                e_stop_score = -accel/e_decel
                if e_stop_score > self._scores_data["e_stop"]:
                    self._scores_data["e_stop"] = e_stop_score

        # COllision
        if traci.simulation.getCollidingVehiclesNumber() > 0:
            if "ego" in traci.simulation.getCollidingVehiclesIDList():
                self._scores_data["collision"] = 1


        return


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
            traci.vehicle.setSpeed(scenicObj.name, scenicObj.speed)

        if scenicObj.lane != 0:
            traci.vehicle.changeLane(scenicObj.name, scenicObj.lane, 3)

        if scenicObj.speedMode != "":
            traci.vehicle.setSpeedMode(scenicObj.name, scenicObj.speedMode)

        if scenicObj.color != "":
            traci.vehicle.setColor(scenicObj.name, scenicObj.color)

        if scenicObj.changeSpeed != "" and scenicObj.changeSpeed[1] == 0:
            traci.vehicle.setSpeed(scenicObj.name, scenicObj.changeSpeed[0])
        
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

            # End if ego is not in the scene
            if not "ego" in traci.vehicle.getIDList():
                break
            
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
                    scenicObj.changeSpeed[1] == traci.simulation.getTime():
                    traci.vehicle.setSpeed(scenicObj.name, scenicObj.changeSpeed[0])

            try:
                self.__update_subscriptions_history()
            except KeyError:
                # Ego is no longer in sim
                break
            self.__score_update()

            if traci.simulation.getTime() > 3600:
                print("Sim time over 1 hour. Ending Scene.")
                return
            
            traci.simulation.step()

        return
        # traci.close()