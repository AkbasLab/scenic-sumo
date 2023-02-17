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