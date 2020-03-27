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

incRadius = 4
incIntensity = 1
intensityMin = 20

initialNbClusters = 3
canvasWidth = 100
canvasHeight = 100
marginX = 10
marginY = 10


# Create rain data
evtMng = EventManager.EventManagerClass()
evtGen = EventGenerator.EventGeneratorClass(initialNbClusters, canvasWidth, canvasHeight, marginX, marginY)

# Construct the scatter which we will update during animation
# as the raindrops develop.
scat = ax.scatter(x=[], y=[], s=[], lw=0.5, edgecolors=(0,0,0,1), facecolors='none')


def update(frame_number):
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

    offsetList, sizeList, intensityList = evtMng.getEventList()

    colorList = np.ones((len(sizeList),4)) * (1,0,0,1)
    colorList[:,3] = [(x -intensityMin)/(centerIntensity-intensityMin) for x in intensityList]

    # Update the scatter collection, with the new colors, sizes and positions.
    scat.set_edgecolors(colorList)
    scat.set_offsets(offsetList)
    scat.set_sizes(sizeList)


# Construct the animation, using the update function as the animation director.
animation = FuncAnimation(fig, update, interval=10)
plt.show()
