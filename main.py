# Module imports
import eventClass as Event
import eventManagerClass as EventManager
import eventGeneratorClass as EventGenerator

# Third party imports
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation


# Settings
generationMode = "Cluster" #"Random" 
nb_clusters = 1
noiseRate = 10
max_x_stdev = 2
max_y_stdev = 2
max_centerX_stdev = 1
max_centerY_stdev = 1
centerIntensity = 100

incRadius = 4
incIntensity = 1
intensityMin = 20

initialNbClusters = 3
canvasWidth = 100
canvasHeight = 100
marginX = 10
marginY = 10

min_cluster_size = 5

# Create new Figure and an Axes which fills it.
fig = plt.figure(figsize=(5, 5))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(0, canvasWidth), ax.set_xticks([])
ax.set_ylim(0, canvasHeight), ax.set_yticks([])

evtMng = EventManager.EventManagerClass()
evtGen = EventGenerator.EventGeneratorClass(initialNbClusters, canvasWidth, canvasHeight, marginX, marginY)

# Construct the scatter which we will update during animation
# as the raindrops develop.
scat = ax.scatter(x=[], y=[], s=[], lw=0.5, edgecolors=(0,0,0,1), facecolors='none')

# https://www.stat.berkeley.edu/~nelle/teaching/2017-visualization/README.html#contour-plots
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
    evtMng.clusterEvents(min_cluster_size)

    offsetList, sizeList, colorList = evtMng.getDataToScatter(centerIntensity, intensityMin)

    # Update the scatter collection, with the new colors, sizes and positions.
    scat.set_offsets(offsetList)
    scat.set_sizes(sizeList)
    scat.set_edgecolors(colorList)

# Construct the animation, using the update function as the animation director.
animation = FuncAnimation(fig, update, interval=10)
plt.show()
