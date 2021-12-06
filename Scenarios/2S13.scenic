from scenic.simulators.sumo.model import *
#from scenic.core.distributions import *

'''Using CurvyRoad.sumocfg'''

ego = Car at 0 @ 0 
ego.name = "v1"
ego.route = ["492300616#0", "159453012"]
ego.color = [255,0,0,255]
ego.speed = 9
ego.xPos = 1648
ego.yPos = 88

NPC1 = Car at 0 @ 2
NPC1.name = "v2"
NPC1.route = ["492300616#0", "159453012"]
NPC1.lane = 1
NPC1.speed = 10
NPC1.xPos = 1645
NPC1.yPos = 88


NPC2 = Car at 0 @ 4
NPC2.name = "v3"
NPC2.route = ["492300616#0","159453012"]
NPC2.xPos = 1639
NPC2.yPos = 163
NPC2.angle = 60
NPC2.speed = 0
NPC2.vehPlacement = 0
