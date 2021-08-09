from scenic.simulators.sumo.model import *

ego = Car at 0 @ 0
ego.name = "v4"
ego.route = ["128953755#2", "128575963#7"]


tl = TrafficLight at 0 @ 3
tl.name = "101071681"
tl.state = "GGGgrrrrGGgg,yyyyrrrryyyy,rrrrrrrrrrrr"
tl.duration = "20,20,20"