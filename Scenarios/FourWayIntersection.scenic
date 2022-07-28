from scenic.simulators.sumo.model import *

ego = Car at 0 @ 2
ego.name = "v1"
ego.route = ["e2", "-e4"]
ego.distance = 10
ego.speedMode = 32
ego.color = [1, 0, 0, 1]
ego.parkPos = ["park", 20]

car2 = Car at 0 @ 0
car2.name = "v2"
car2.route = ["e2", "-e3"]
car2.speed = 20
#car2.changeSpeed = [25 , 2]
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

car4 = Car at 2 @ 4
car4.name = "v4"
car4.route = ["e1", "-e4"]
car4.speedMode = 32
car4.parkPos = ["park", 20]

car5 = Car at 4 @ 0
car5.name = "v5"
car5.route = ["e1", "-e4"]
car5.speedMode = 32
car5.parkPos = ["park", 20]
car5.distance = 10

tl = TrafficLight at 2 @ 0
tl.name = "gneJ1"
tl.state = "GGGgrrrrGGGgrrrr,yyyyrrrryyyyrrrr,rrrrGGGgrrrrGGGg"
tl.duration = "20,20,20"

pa = ParkingLot at 2 @ 2
pa.name = "park"
pa.lane = "-e4_0"
pa.startPos = 0
pa.endPos = 50
pa.capacity = 5

