from scenic.simulators.sumo.model import *

‘’’Using simple.sumocfg’’’

ego = Car at 0 @ 0
ego.name = “av”
ego.route = [“-E1”,”-E0”,”-Ewarmup”]
ego.speedMode = 32
ego.tau = 0.1
ego.speed = 10