from scenic.simulators.sumo.model import *

ego = Car at 0 @ 0
ego.name = "v1"
ego.route = ["515643153", "515643150"]

car1 = Car at 0 @ 2
car1.name = "v2"
car1.route = ["515643140#1","515643141#0"]

ped = Pedestrian at 0 @ 4
ped.name = "Bob"
ped.route = ["515644342#2","515644344#2"]