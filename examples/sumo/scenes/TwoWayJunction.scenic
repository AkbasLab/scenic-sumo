from scenic.simulators.sumo.model import *

class RandomCar(Car): 
    """Random distance"""
    randomDistance: Range(0,1000)
    randomSpeed: Range(0,100)

ego = RandomCar at 0 @ 2
ego.name = "v2"
ego.route = ["E2", "E3"]

Car1 = RandomCar at 0 @ 0
Car1.name = "v3"
Car1.route = ["E1", "E3"]
