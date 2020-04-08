# Module imports
import eventClass as Event
import eventManagerClass as EventManager
import eventGeneratorClass as EventGenerator

# Third party imports
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

# Settings
generationMode = "Cluster" #"Random" 
nb_clusters = 1
noiseRate = 10
max_x_stdev = 2
max_y_stdev = 2
max_centerX_stdev = 2
max_centerY_stdev = 2
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
min_proba_cluster = 0

# definitions for the axes
left, width = 0.2, 0.65
bottom, height = 0.3, 0.65
spacing = 0.02


# Create new Figure and Axes which fill it.
fig = plt.figure(figsize=(5, 5))

ax_scatter = plt.axes([left, bottom, width, height])
ax_scatter.set_xlim(0, canvasWidth)
ax_scatter.set_ylim(0, canvasHeight)

slider_incIntensity_ax = plt.axes([left, 0.05 + spacing, width, 0.02])
slider_MinProba_ax = plt.axes([left, 0.1 + spacing, width, 0.02])
#slider_IntDecrease_ax = plt.axes([left, 0.15 + spacing, width, 0.02])

plt.axes(ax_scatter)
plt.title('Datastream clustering')

#intMin_slider = Slider(slider_IntMin_ax,'Intensity Min',0, 255,valinit=200)
minProba_slider = Slider(slider_MinProba_ax,'Proba minimum',0, 1, valinit=min_proba_cluster, valstep=0.1)
incIntensity_slider = Slider(slider_incIntensity_ax,'Intensity decrease Speed',0, 5, valinit=incIntensity, valstep=0.1)


evtMng = EventManager.EventManagerClass()
evtGen = EventGenerator.EventGeneratorClass(initialNbClusters, canvasWidth, canvasHeight, marginX, marginY)

# Construct the scatter which we will update during animation
# as the raindrops develop.
scat = ax_scatter.scatter(x=[], y=[], s=[], lw=0.5, edgecolors=(0,0,0,1), facecolors='none')


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
    evtMng.updateEventsShape(incRadius, incIntensity_slider.val) 
    evtMng.removeWeakEvents(intensityMin)
    evtMng.clusterEvents(min_cluster_size, minProba_slider.val)

    offsetList, sizeList, colorList = evtMng.getDataToScatter(centerIntensity, intensityMin)

    #print(offsetList)
    #print(sizeList)
    #print(colorList)

    # Update the scatter collection, with the new positions, sizes, colors.
    scat.set_offsets(offsetList)
    scat.set_sizes(sizeList)
    scat.set_edgecolors(colorList)

# Construct the animation, using the update function as the animation director.
animation = FuncAnimation(fig, update, interval=10)
plt.show()
