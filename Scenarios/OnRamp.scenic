from scenic.simulators.sumo.model import *

ego = Car at 0 @ 0
ego.name = "v1"
ego.route = ["482125987#1", "83336631#1"]

car1 = Car at 0 @ 2
car1.name = "v2"
car1.route = ["11355503","87853223#3"]

tl = TrafficLight at 2 @ 0
tl.name = "101035693"
tl.state = "rrGG,rryy,GGrr,yyrr"
tl.duration = "39,6,39,6"