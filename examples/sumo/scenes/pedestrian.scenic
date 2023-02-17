from scenic.simulators.sumo.model import *
from scenic.core.distributions import *
import random

model scenic.simulators.sumo.model

'''Using CurvyRoad.sumocfg'''

kph2mps = 1/3.6

the_route = ["492300616#0", "159453012"]
lanes = [0,1]
ego_lane = random.choice(lanes)
lanes.remove(ego_lane)
npc1_lane = random.choice(lanes)
ego_dist = 100

ego = Car at 0 @ 0, 
    with lane ego_lane,
    with distance ego_dist,
    with track True,
    with route the_route,
    with name "ego",
    with color [255,0,0,255],
    with speed Range(1,100) * kph2mps

npc1 = Car at 0 @ 2,
    with name "npc1",
    with lane npc1_lane,
    with color [255,255,0,255],
    with distance Range(-100,100) + ego_dist,
    with route the_route,
    with speed Range(0,100) * kph2mps,
    with laneChange [ego_lane, Range(0,60)]

npc2 = Car at 0 @ 4,
    with name "npc2",
    with lane ego_lane,
    with color [255,255,0,255],
    with distance Range(-100,-10) + ego_dist,
    with route the_route,
    with speed Range(0, 100) * kph2mps

tl = TrafficLight at 0 @ 6,
    with name "1423875783",
    with state ["rrrrGGrrrrrrrr","rrrryyrrrrrrrr","rrrrrrrrrrrrrr"],
    with duration [Range(1,30),Range(0,10),Range(1,30)]

ped_route = ["492300618#0", "-128973657#1"]
start_of_inter = 114.63

peds = []
ped_dist_from_inter = []
for i in range(3):
    dist_from_inter = Range(0,50)
    ped = Pedestrian at 0 @ (8+2*i),
        with name "ped_%d" % i,
        with route ped_route,
        with color [255,255,0,255],
        with departTime Range(0,40),
        with distance start_of_inter - dist_from_inter,
        with egoWaitAtXing True
    peds.append(ped)
    ped_dist_from_inter.append(dist_from_inter)

param ego_lane = ego.lane
param ego_speed = ego.speed

param npc1_lane = npc1.lane
param npc1_distance = npc1.distance
param npc1_speed = npc1.speed
param npc1_laneChange = npc1.laneChange[1]

param npc2_lane = npc2.lane
param npc2_distance = npc2.distance
param npc2_speed = npc2.speed

param tl_g = tl.duration[0]
param tl_y = tl.duration[1]
param tl_r = tl.duration[2]

param peds_departTime = [ped.departTime for ped in peds]
param peds_distance = [dist for dist in ped_dist_from_inter]