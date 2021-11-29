'''
Notes: 
The car does not process the raod when using a randomCar 
but does register the road when the Car is used. Checked 
Netedit road and it says they're connected. 
'''
from scenic.simulators.sumo.model import *

class RandomCar(Car):
    randomDistance: Range(0,100)
    randomSpeed: Range(0,100)

ego = Car at 0 @ 0
ego.name = "v1"
ego.route = ["482125987#1", "83336631#1"]
'''
randomCar = RandomCar at 0 @ 4
randomCar.name = "v3"
randomCar.route = ["11355503", "83336631#1"]
randomCar.speedMode = 32
'''
car1 = Car at 0 @ 2
car1.name = "v2"
car1.route = ["11355503","87853223#3"]

tl = TrafficLight at 2 @ 0
tl.name = "101035693"
tl.state = "rrGG,rryy,GGrr,yyrr"
tl.duration = "39,6,39,6"