from scenic.simulators.sumo.model import *

ego = Car at 0 @ 0
ego.name = "v1"
ego.route = ["492300616#0","159453012"]
ego.speed = 12

NPC1 = Car at 0 @ 2
NPC1.name = "v2"
NPC1.route = ["492300616#0","159453012"]
NPC1.color = [255,0,0,255]
NPC1.speed = 20
NPC1.changeSpeed = [25, 20]