from scenic.simulators.sumo.model import *

hello = Car at 2 @ 0
hello.name = "v3"
hello.route = ["e1", "-e5"]

ego = Car at 2 @ 2
ego.name = "v2"
ego.route = ["e2", "-e4"]

tl_1 = TrafficLight at 0 @ 2
tl_1.name = "gneJ1"
tl_1.state = "gGGgrrrrgGGgrrrrrGrG,yyyyrrrryyyyrrrrryry,rrrrgGGgrrrrgGGgGrGr"
tl_1.duration = "20,10,20"

tl_2 = TrafficLight at 0 @ 0
tl_2.name = "gneJ6"
tl_2.state = "gGGgrrrrgGGgrrrrrGrG,yyyyrrrryyyyrrrrryry,rrrrgGGgrrrrgGGgGrGr"
tl_2.duration = "20,10,20"

person = Pedestrian at 2 @ 4
person.name = "Bill"
person.route = ["e1", "e2"]

ped = Pedestrian at 4 @ 0
ped.name = "Peter"
ped.route = ["e2", "e5"]
