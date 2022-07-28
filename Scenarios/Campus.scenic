from scenic.simulators.sumo.model import *

'''
NPC1 accelerates in the lane on DUT's right side until it is 
ahead of DUT. Starts on right side of DUT.
'''

ego = Car at 0 @ 0
ego.name = "v1"
ego.route = ["492300616#0", "159453012"]
ego.lane = 1
ego.speed = 10

NPC1 = Car at 0 @ 2
NPC1.name = "v2"
NPC1.lane = 0
NPC1.route = ["492300616#0","159453012"]
NPC1.changeSpeed = [30,5]
NPC1.color = [1,0,0,1]
NPC1.laneMode = 512
NPC1.laneChanges = [1 ,30]
NPC1.track = 1

random = RandomTrips at 0 @ 4
