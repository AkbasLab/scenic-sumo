from scenic.simulators.sumo.model import *

'''Using CurvyRoad.sumocfg'''

ego = Car at 0 @ 0
ego.name = "v1"
ego.lane = 0
ego.route = ["492300616#0", "159453012"]

NPC1 = Car at 0 @ 2
NPC1.name = "v2"
NPC1.route = ["492300616#0", "159453012"]
NPC1.lane = 1
NPC1.xPos = 1632
NPC1.yPos = 146
NPC1.laneChanges = [0, 10]
NPC1.color = [255,0,0,255]