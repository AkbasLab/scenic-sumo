from scenic.simulators.sumo.model import *

ego = Car at 3 @ 2
ego.name = "v2"
ego.route = ["e2", "e3"]

Car2 = Car
Car2.name = "v1"
Car2.route = ["e1", "e3"]
Car2.distance = 60

#car2 = Car at 1 @ 2, facing 0 deg, with viewAngle 30 deg
"""Biker at 0 @ 2"""
"""car2 = Car offset by Range(-10, 10) @ Range(20, 40), with viewAngle 30 deg
require car2 can see ego"""