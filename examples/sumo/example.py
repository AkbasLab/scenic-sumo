import os
FILE_DIR = os.path.dirname(os.path.abspath(__file__))

import warnings
warnings.filterwarnings("ignore", category=UserWarning) 

import scenic
import json
from scenic.simulators.sumo.simulator import SumoSimulator
import pandas as pd


def describe(
    car, 
    features : list = ["name", "route", "distance", "lane",
        "speed","speedMode","color","changeSpeed","tau",
        "parkPos","laneMode","laneChanges","routeID"],
    show : bool = False
    ) -> str:
        d = {}
        for key, val in car.__dict__.items():
            if key in features:
                d[key] = val

        if show:
            pretty = json.dumps(d, sort_keys=True, indent=2)
            print(pretty)
        return d

def mps2kph(mps : float) -> float:
    return mps * 3.6

class Example:
    def __init__(self):
        self._error_log = "%s/error-log.txt" % (FILE_DIR)

        config = {
            
            # "gui" : False,
            "gui" : True,
            
            #Collisions
            "--collision.action" : "warn",
            "--collision.check-junctions": "", 
            "--collision.stoptime": 50,

            # Logging
            "--error-log" : self._error_log,

            # Smooth lane changing
            "--lanechange.duration": 2,

            # Traci Connection
            # "--num-clients" : 1,

            # GUI Options
            "--delay" : 100,
            "--start" : "--quit-on-end",

            # RNG
            "--seed" : 333
        
        }

        
        scene_fn = "%s/scenes/pedestrian.scenic" % (FILE_DIR)
        map_fn = "%s/maps/CurvyRoad.net.xml" % (FILE_DIR)
        simulator = SumoSimulator(map_fn, scene_fn, config)

        errors = [self.read_errors()]


        # return

        for i in range(1000-1):
            simulator.createSimulation()
            errors.append(self.read_errors())
            continue




        
        df = pd.DataFrame({
            "run" : [i for i in range(len(errors))],
            "params" : [scene.params for scene in simulator.scenes],
            "errors" : errors
        })

        df["xing"] = [sim.ped_ego_wait_at_xing_event for sim in simulator.sims]

        fn = "%s/out/tests.feather" % FILE_DIR
        df.to_feather(fn)
        df = pd.read_feather(fn)
        print(df)
        
        return


    def read_errors(self) -> list:
        with open(self._error_log, "r") as f:
            errors = f.readlines()
        return errors




if __name__ == "__main__":
    Example()