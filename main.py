# Module imports
import eventManagerClass as EventManager
import eventGeneratorClass as EventGenerator

# Third party imports
import numpy as np
import json
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
import matplotlib.gridspec as gridspec



with open("initParam.json", "r") as read_file:
    defaultParams = json.load(read_file)

# Settings
generationMode = defaultParams["generationMode"]
nb_clusters = defaultParams["nb_clusters"]
noiseRate = defaultParams["noiseRate"]
max_x_stdev = defaultParams["max_x_stdev"]
max_y_stdev = defaultParams["max_y_stdev"]
max_centerX_stdev = defaultParams["max_centerX_stdev"]
max_centerY_stdev = defaultParams["max_centerY_stdev"]
centerIntensity = defaultParams["centerIntensity"]

incRadius = defaultParams["incRadius"]
incIntensity = defaultParams["incIntensity"]
intensityMin = defaultParams["intensityMin"]

initialNbClusters = defaultParams["initialNbClusters"]
canvasWidth = defaultParams["canvasWidth"]
canvasHeight = defaultParams["canvasHeight"]
marginX = defaultParams["marginX"]
marginY = defaultParams["marginY"]

min_cluster_size = defaultParams["min_cluster_size"]
min_proba_cluster = defaultParams["min_proba_cluster"]
roundPersistence = defaultParams["roundPersistence"] # 1 decimale
lifeTimeFilter = defaultParams["lifeTimeFilter"]  # Number minimum of lifeTime to display

# Create new Figure
fig, axes = plt.subplots(figsize=(10, 6))
fig.canvas.set_window_title('Cluster detection & persistence analysis') 
spec = gridspec.GridSpec(ncols=2, nrows=6, height_ratios=[30, 1, 1, 1, 1, 1], wspace = 0.3, hspace = 0.15)
axes.axis("off")

# Scatter Plot of 2d input
ax_scatter = fig.add_subplot(spec[0, 0])
ax_scatter.set_xlim(0, canvasWidth)
ax_scatter.set_ylim(0, canvasHeight)
ax_scatter.set_xlabel("x")
ax_scatter.set_ylabel("y")
ax_scatter.set_aspect('equal')
ax_scatter.set_title('Cluster detection of 2d input')

scat = ax_scatter.scatter(x=[], y=[], s=[], lw=0.5, edgecolors=(0,0,0,1), facecolors='none')

# Bar Plot for showing persistence to each cluster detected
ax_bar = fig.add_subplot(spec[0, 1])

# Sliders Plot for chart settings
minProba_slider = Slider(fig.add_subplot(spec[3, 0]),'Clustering \nproba min',0, 1, valinit=min_proba_cluster, valstep=0.1)
minProba_slider.label.set_size(8)

incIntensity_slider = Slider(fig.add_subplot(spec[4, 0]),'Intensity \ndecrease',0, 5, valinit=incIntensity, valstep=0.1)
incIntensity_slider.label.set_size(8)

noise_slider = Slider(fig.add_subplot(spec[5, 0]),'Noise Rate',0, 100, valinit=noiseRate, valstep=1)
noise_slider.label.set_size(8)

lifeTimeFilter_slider = Slider(fig.add_subplot(spec[4, 1]),'Life Time \nFilter',0, 100, valinit=lifeTimeFilter, valstep=5)
lifeTimeFilter_slider.label.set_size(8)

# Use to generate event & detect cluster & return data to display
evtMng = EventManager.EventManagerClass()
evtGen = EventGenerator.EventGeneratorClass(initialNbClusters, canvasWidth, canvasHeight, marginX, marginY)

# Add event on the Scatter plot by clicking
def onclick(event):
    if event.inaxes != ax_scatter: return
    #print(u"event.x :", event.xdata  , '  event.y:', event.ydata)
    evtMng.createEvent(event.xdata, event.ydata, centerIntensity)

cid = fig.canvas.mpl_connect('button_press_event', onclick)

def update(frame_number):
    event = evtGen.createEvent(
        generationMode,
        nb_clusters,
        noise_slider.val,
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

    # Update the scatter collection, with the new positions, sizes, colors.
    scat.set_offsets(offsetList)
    scat.set_sizes(sizeList)
    scat.set_edgecolors(colorList)

    IdList, lifeTimeList, persistenceList, cluster_colors = evtMng.getDataToPlot(roundPersistence, lifeTimeFilter_slider.val)

    # Refresh the bar, with the new positions, height, colors.
    ax_bar.clear()
    ax_bar.set_title('Clusters persistence')
    ax_bar.set_xlabel("Cluster ID")
    ax_bar.set_ylabel("Persistence score (Stability)")
    ax_bar.set_ylim(0, 1)
    ax_bar.set_xlim(-0.5, 10)
    ax_bar.set_xticks(range(10))
    ax_bar.bar(x=IdList, height=persistenceList, color=cluster_colors)

# Construct the animation, using the update function as the animation director.
animation = FuncAnimation(fig, update, interval=10)
plt.show()
