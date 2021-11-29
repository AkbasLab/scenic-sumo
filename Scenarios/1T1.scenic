from scenic.simulators.sumo.model import *

ego = Car at 0 @ 0 
ego.name = "v1"
ego.route = ["gneE3","-gneE1"]

NPC1 = Car at 0 @ 2
NPC1.name = "v2"
NPC1.route = ["gneE2","-gneE0"]
NPC1.changeSpeed = [20, 0, 10]
NPC1.speedMode = 32