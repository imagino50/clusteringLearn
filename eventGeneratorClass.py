# Module imports
import eventClass as Event

# Third party imports
import numpy as np
import random

# Fixing random state for reproducibility
#np.random.seed(19680801)

class EventGeneratorClass:
  class ClusterCenter:
        def __init__(self, x,y ):
            self.x = x
            self.y = y

# =============================================================================
# __init__() functions as the class constructor
# =============================================================================
  def __init__(self, initialNbClusters, canvasWidth, canvasHeight, marginX, marginY):
    self.marginX = marginX
    self.marginY = marginY
    self.width = canvasWidth - marginX
    self.height = canvasHeight - marginY
    self.clusterCenterList = []
    self._initClusterCenterList_(initialNbClusters)


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

      self.updateRandomClusterCenter(
        max_centerX_stdev,
        max_centerY_stdev
      )

      #self.updateNumberClusters(nb_clusters)
      #print(event.x)
      #print(event.y)
      return event


  #=============================================================================
  # Generate an event either randomly or clustered
  #=============================================================================
  def _generateEvent_(self, noiseRate, centerIntensity, max_x_stdev, max_y_stdev):
    rand = random.randint(0, 100)
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
    clusterCenter = EventGeneratorClass.ClusterCenter(random.randrange(self.marginX, self.width), random.randrange(self.marginY, self.height))
    self.clusterCenterList.append(clusterCenter)


  #=============================================================================
  # Create Event at ramdom position
  #=============================================================================
  def _createRandomEvent_(self, centerIntensity):
    return Event.EventClass(
      # randomly select a number between 0-self.width 
      random.randrange(self.marginX, self.width),
      # randomly select a number between 0-self.height 
      random.randrange(self.marginY, self.height),
      centerIntensity
    )
  

  #=============================================================================
  # Create an Event clustered
  #=============================================================================
  def _createClusteredEvent_(self, cluster, centerIntensity, max_x_stdev, max_y_stdev):
    return Event.EventClass(
      round(np.random.normal(cluster.y, max_y_stdev)), 
      round(np.random.normal(cluster.x, max_x_stdev)), 
      centerIntensity
    )

  
  #=============================================================================
  # Update a center of a cluster choosed randomly
  #=============================================================================
  def updateRandomClusterCenter(self, max_centerX_stdev, max_centerY_stdev):
    if len(self.clusterCenterList) > 0:
      clusterId = random.randrange(0, len(self.clusterCenterList))

      newPosX = round(np.random.normal(
        self.clusterCenterList[clusterId].x,
        max_centerX_stdev
      ))
      if (newPosX > 0) and (newPosX < self.width):
        self.clusterCenterList[clusterId].x = newPosX
      
      newPosY = round(np.random.normal(
        self.clusterCenterList[clusterId].y,
        max_centerY_stdev
      ))
      if (newPosY > 0) and (newPosY < self.height):
        self.clusterCenterList[clusterId].y = newPosY
       

  #=============================================================================
  # Update the numbers of clusters
  #=============================================================================
  def updateNumberClusters(self, nb_clusters):
    current_nb_clusters = len(self.clusterCenterList)
    if current_nb_clusters < nb_clusters:
      for _ in range(nb_clusters - current_nb_clusters):
        self._addRandomClusterCenter_()
    elif (current_nb_clusters > nb_clusters):
      for i in range(current_nb_clusters - nb_clusters):
        self.clusterCenterList.pop(i)




