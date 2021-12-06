from scenic.simulators.sumo.model import *

'''Using 1X.sumocfg'''

ego = Car at 0 @ 0
ego.name = "v1"
ego.route = ["gneE0","-gneE2"]
ego.speedMode = 32
ego.tau = 0.1
ego.speed = 10

NPC1 = Car at 0 @ 2
NPC1.name = "v2"
NPC1.route = ["gneE3","-gneE1"]
NPC1.speedMode = 32
NPC1.tau = 0.1
NPC1.speed = 9.5