import scenic
import matplotlib.pyplot as plt
import seaborn as sns


i = 0
y = []
while(i < 50):

    scenario = scenic.scenarioFromFile("C:\\Users\\crump\\AppData\\Local\\Programs\\Python\\Python38\\Lib\\scenic\\simulators\\sumo\\Scenarios\\distribution.scenic")

    #Grabs scene from the scenario
    scene = scenario.generate(maxIterations = 1, verbosity = 0, feedback = None)

    for scenicObj in scene[0].objects:
        #Appends each scenarios value to a list 
        y.append(scenicObj.normal)

    i+=1
#Displays list
sns.displot(y, bins=100)
plt.show()
#plt.savefig("filename.png")
