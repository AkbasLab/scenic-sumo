import os, sys
import scenic

scenario = scenic.scenarioFromFile("C:\\Users\crump\\OneDrive\\Documents\\GitHub\\Scenic-Sumo\\behindCarWithPedestrian.scenic")

scene = scenario.generate(maxIterations = 200, verbosity = 0, feedback = None)

#Prints all of tge data in the scene
#print(scene[0].objects[0])
print(scene[0].objects)

#C:\Users\crump\AppData\Local\Programs\Python\Python38\Lib\scenic\simulators\sumo
