# Module imports
import eventClass as Event

# Third party imports
import numpy as np
import pandas as pd
import collections
import random

class EventGeneratorClass:
  class ClusterCenter:
        def __init__(self, x,y ):
            self.x = x
            self.y = y

# =============================================================================
# __init__() functions as the class constructor
# =============================================================================
  def __init__(self, initialNbClusters, canvasWidth, canvasHeight, marginX, marginY):
    self.width = canvasWidth - marginX
    self.height = canvasHeight - marginY
    self.clusterCenterList = []
    self._initClusterCenterList_(initialNbClusters)

    #for i in range(len(self.clusterCenterList)): 
      #print(self.clusterCenterList[i].x)
      #print(self.clusterCenterList[i].y)

  #=============================================================================
  # Init List of center cluster
  #=============================================================================
  def _initClusterCenterList_(self, initialNbClusters):
    self.clusterCenterList = []
    for _ in range(initialNbClusters):
      self._addRandomClusterCenter_()
      

  #=============================================================================
  # Main function : Add an event as noise or related to a cluster
  #=============================================================================
  def createEvent(
    self,
    generationMode,
    nb_clusters,
    noiseRate,
    max_x_stdev,
    max_y_stdev,
    max_centerX_stdev,
    max_centerY_stdev,
    centerIntensity
  ): 
    if (generationMode == "Random"):
      return self._createRandomEvent_(centerIntensity)
    elif (generationMode == "Cluster"):
      event = self._generateEvent_(
        noiseRate,
        centerIntensity,
        max_x_stdev,
        max_y_stdev
      )
      return event
      #self.addEvent(event)


  #=============================================================================
  # Generate an event either randomly or clustered
  #=============================================================================
  def _generateEvent_(self, noiseRate, centerIntensity, max_x_stdev, max_y_stdev):
    rand = random.randrange(0, 100)
    if (rand < noiseRate):
      return self._createRandomEvent_(centerIntensity)
    elif (len(self.clusterCenterList) > 0):
      clusterId = random.randrange(0, len(self.clusterCenterList))
      return self._createClusteredEvent_(
        self.clusterCenterList[clusterId],
        centerIntensity,
        max_x_stdev,
        max_y_stdev
      )


  #=============================================================================
  # Add randomly a cluster center
  #=============================================================================
  def _addRandomClusterCenter_(self):
    clusterCenter = EventGeneratorClass.ClusterCenter(random.randrange(0, self.width), random.randrange(0, self.height))
    self.clusterCenterList.append(clusterCenter)


  #=============================================================================
  # Create Event at ramdom position
  #=============================================================================
  def _createRandomEvent_(self, centerIntensity):
    return Event.EventClass(
      # randomly select a number between 0-self.width 
      random.randrange(self.width),
      # randomly select a number between 0-self.height 
      random.randrange(self.height),
      centerIntensity
    )
  

  #=============================================================================
  # Create an Event clustered
  #=============================================================================
  def _createClusteredEvent_(self, cluster, centerIntensity, max_x_stdev, max_y_stdev):
    return Event.EventClass(
      np.random.normal(cluster.y, max_y_stdev), #(cluster.y, max_y_stdev),
      np.random.normal(cluster.x, max_x_stdev), #round(cluster.x, max_x_stdev),
      centerIntensity
    )
  
 


