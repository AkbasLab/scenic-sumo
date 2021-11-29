from scenic.simulators.sumo.model import *

class RandomCar(Car):
    randomDistance: Range(0,100)
    randomSpeed: Range(10,20)

ego = RandomCar at 0 @ 0
ego.name = "v1"
ego.route = ["gneE0", "gneE1"]