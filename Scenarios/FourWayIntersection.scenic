from scenic.simulators.sumo.model import *

hello = Car at 3 @ -1
hello.name = "v3"
hello.route = ["e1", "-e3"]

ego = Car at 3 @ 2
ego.name = "v2"
ego.route = ["e2", "-e4"]

tl = TrafficLight at 1 @ 0
tl.name = "gneJ1"
tl.state = "GGGgrrrrGGGgrrrr,yyyyrrrryyyyrrrr,rrrrGGGgrrrrGGGg"
tl.duration = "20,20,20"