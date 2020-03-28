# Module imports
import eventClass as Event
import eventManagerClass as EventManager
import eventGeneratorClass as EventGenerator

# Third party imports
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import seaborn as sns

# Fixing random state for reproducibility
#np.random.seed(19680801)

# Settings
generationMode = "Cluster" #"Random" 
nb_clusters = 1
noiseRate = 20
max_x_stdev = 2
max_y_stdev = 2
max_centerX_stdev = 0
max_centerY_stdev = 0
centerIntensity = 100

incRadius = 4
incIntensity = 1
intensityMin = 20

initialNbClusters = 3
canvasWidth = 50
canvasHeight = 50
marginX = 10
marginY = 10

# Create new Figure and an Axes which fills it.
fig = plt.figure(figsize=(5, 5))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(0, canvasWidth), ax.set_xticks([])
ax.set_ylim(0, canvasHeight), ax.set_yticks([])

sns.set_color_codes()
# https://seaborn.pydata.org/tutorial/color_palettes.html
color_palette = sns.color_palette('deep') #bright
r =  [x[0] for x in color_palette]
g =  [x[1] for x in color_palette]
b =  [x[2] for x in color_palette]
#print(color_palette)

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
    evtMng.clusterEvents()

    offsetList, sizeList = evtMng.getDataToScatter()
    eventList = evtMng.getEventList()

    r1 = [r[event.clusterId] if event.clusterId >= 0 else 0.0 for event in eventList]
    g1 = [g[event.clusterId] if event.clusterId >= 0 else 0.0 for event in eventList]
    b1 = [b[event.clusterId] if event.clusterId >= 0 else 0.0 for event in eventList]
    a = [(event.intensity - intensityMin)/(centerIntensity - intensityMin) for event in eventList]
    colorList = tuple(zip(r1, g1, b1, a))

    # Update the scatter collection, with the new colors, sizes and positions.
    scat.set_edgecolors(colorList)
    scat.set_offsets(offsetList)
    scat.set_sizes(sizeList)


# Construct the animation, using the update function as the animation director.
animation = FuncAnimation(fig, update, interval=10)
plt.show()
