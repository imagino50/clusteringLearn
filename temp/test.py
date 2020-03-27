# Module imports
import eventClass as Event
import eventManagerClass as EventManager
import eventGeneratorClass as EventGenerator

# Third party imports
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

# Fixing random state for reproducibility
#np.random.seed(19680801)


# Create new Figure and an Axes which fills it.
fig = plt.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(0, 100), ax.set_xticks([])
ax.set_ylim(0, 100), ax.set_yticks([])

# Settings
generationMode = "Random"
nb_clusters = 3
noiseRate = 20
max_x_stdev = 5
max_y_stdev = 5
max_centerX_stdev = 5
max_centerY_stdev = 5
centerIntensity = 100

incRadius = 2
incIntensity = 2
intensityMin = 20

initialNbClusters = 3
canvasWidth = 100
canvasHeight = 100
marginX = 10
marginY = 10

# Create rain data
evtMng = EventManager.EventManagerClass()
evtGen = EventGenerator.EventGeneratorClass(initialNbClusters, canvasWidth, canvasHeight, marginX, marginY)

x = [5,7,8,7,80,17,2,9,4,11,12,9,6]
y = [99,86,87,88,111,86,103,87,94,78,77,85,86]
#colors = (0,0,0)

# Construct the scatter which we will update during animation
# as the raindrops develop.
#plt.scatter(x, y, s=30, lw=0.5, edgecolors=(0,0,0,1), facecolors='none')
scat = ax.scatter(x=[], y=[], s=50, lw=0.5, edgecolors=[], facecolors='none')


event = evtGen.createEvent(
    generationMode,
    nb_clusters,
    noiseRate,
    max_x_stdev,
    max_y_stdev,
    max_centerX_stdev,
    max_centerY_stdev,
    centerIntensity
)
evtMng.addEvent(event)
evtMng.updateEventsShape(incRadius, incIntensity)
evtMng.removeWeakEvents(intensityMin)
offsetList, sizeList = evtMng.getEventList()

color = np.ones((len(sizeList),4)) * (0,0,0,1)
#print("Start...")
#P = np.random.uniform(0,1,(10,2))
#S = np.linspace(0, 20, 10)
print(color)
print(offsetList)
print(sizeList)



# Update the scatter collection, with the new colors, sizes and positions.
scat.set_edgecolors(color)
scat.set_offsets(offsetList)
scat.set_sizes(sizeList)
#scat.set_edgecolors(colors)
#scat.set_offsets(np.hstack((x,y)))
#scat.set_sizes(sizeList)

#plt.title('Matplot scatter plot')
#plt.legend(loc=2)
plt.show()