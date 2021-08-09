from scenic.simulators.sumo.model import *

ego = Car at 0 @ 2
ego.name = "v1"
ego.route = ["e2", "-e4"]
ego.distance = 10
ego.speedMode = 32
ego.color = [255, 0, 0, 255]

car2 = Car at 0 @ 0
car2.name = "v2"
car2.route = ["e2", "-e3"]
car2.speed = 20
car2.changeSpeed = [25 , 2]
car2.speedMode = 32
car2.tau = .1
car2.carParam = 1

car3 = Car at 0 @ 4
car3.name = "v3"
car3.route = ["e1", "-e2"]
car3.xPos = 1
car3.yPos = -10
car3.angle = 60
car3.speed = 0
car3.vehPlacement = 1
car3.speedMode = 32

tl = TrafficLight at 2 @ 0
tl.name = "gneJ1"
tl.state = "GGGgrrrrGGGgrrrr,yyyyrrrryyyyrrrr,rrrrGGGgrrrrGGGg"
tl.duration = [20,20,20]