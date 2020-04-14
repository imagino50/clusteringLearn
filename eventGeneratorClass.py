# Module imports
import eventClass as Event

# Third party imports
import numpy as np
from sklearn import datasets
from sklearn import preprocessing
import pandas as pd
import random

# Fixing random state for reproducibility
#np.random.seed(19680801)

class EventGeneratorClass:

  # =============================================================================
  # Cluster center inner class
  # =============================================================================
  class ClusterCenter:
        # =============================================================================
        # __init__() functions as the class constructor
        # =============================================================================
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
    self.__initClusterCenterList(initialNbClusters)
    self.irisDataset = self.__initDataset()
    self.irisIndex = 0


  #=============================================================================
  # Init List of center cluster
  #=============================================================================
  def __initClusterCenterList(self, initialNbClusters):
    self.clusterCenterList = []
    for _ in range(initialNbClusters):
      self.__addRandomClusterCenter()
      
    
  #=============================================================================
  # Init Iris dataset
  #=============================================================================
  def __initDataset(self):
    # load_wine([return_X_y])
    # load_breast_cancer([return_X_y])
    # load_digits([n_class, return_X_y])
    dataBunch = datasets.load_iris(return_X_y=False)
    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, self.width + self.marginX))
    data_scaled = min_max_scaler.fit_transform(dataBunch.data)
    #df = pd.DataFrame(data_scaled, columns=['Sepal_Length','Sepal_width','Petal_Length','Petal_width']).round()
    df = pd.DataFrame(data_scaled, columns=dataBunch.feature_names).round()
    df = df.sample(frac=1).reset_index(drop=True)
    print(dataBunch.feature_names)
    print(df)
    return df


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
      event = self.__createRandomEvent(centerIntensity)
    elif (generationMode == "Iris"):
      event = self.__createIrisEvent(centerIntensity)
    elif (generationMode == "Cluster"):
      event = self.__generateEvent(
        noiseRate,
        centerIntensity,
        max_x_stdev,
        max_y_stdev
      )

      self.updateRandomClusterCenter(
        max_centerX_stdev,
        max_centerY_stdev
      )

    #print(event.x)
    #print(event.y)
    return event


  #=============================================================================
  # Create an event from Iris dataset
  #=============================================================================
  def __createIrisEvent(self, centerIntensity):
      event = Event.EventClass(self.irisDataset.at[self.irisIndex,'sepal length (cm)'], self.irisDataset.at[self.irisIndex,'sepal width (cm)'], centerIntensity)
      if self.irisIndex < len(self.irisDataset.index)-1:
        self.irisIndex += 1
      else: 
        self.irisDataset = self.irisDataset.sample(frac=1).reset_index(drop=True)
        self.irisIndex = 0

      return event


  #=============================================================================
  # Generate a either clustered event or a random event according to the noise ratio
  #=============================================================================
  def __generateEvent(self, noiseRate, centerIntensity, max_x_stdev, max_y_stdev):
    rand = random.randint(0, 100)
    if (rand < noiseRate):
      return self.__createRandomEvent(centerIntensity)
    elif (len(self.clusterCenterList) > 0):
      clusterId = random.randrange(0, len(self.clusterCenterList))
      return self.__createClusteredEvent(
        self.clusterCenterList[clusterId],
        centerIntensity,
        max_x_stdev,
        max_y_stdev
      )


  #=============================================================================
  # Add randomly a cluster center
  #=============================================================================
  def __addRandomClusterCenter(self):
    clusterCenter = EventGeneratorClass.ClusterCenter(random.randrange(self.marginX, self.width), random.randrange(self.marginY, self.height))
    self.clusterCenterList.append(clusterCenter)


  #=============================================================================
  # Create Event at ramdom position
  #=============================================================================
  def __createRandomEvent(self, centerIntensity):
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
  def __createClusteredEvent(self, cluster, centerIntensity, max_x_stdev, max_y_stdev):
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
      if (newPosX > self.marginX) and (newPosX < self.width):
        self.clusterCenterList[clusterId].x = newPosX
      
      newPosY = round(np.random.normal(
        self.clusterCenterList[clusterId].y,
        max_centerY_stdev
      ))
      if (newPosY > self.marginY) and (newPosY < self.height):
        self.clusterCenterList[clusterId].y = newPosY
       

  #=============================================================================
  # Update the numbers of clusters
  #=============================================================================
  def updateNumberClusters(self, nb_clusters):
    current_nb_clusters = len(self.clusterCenterList)
    if current_nb_clusters < nb_clusters:
      for _ in range(nb_clusters - current_nb_clusters):
        self.__addRandomClusterCenter()
    elif (current_nb_clusters > nb_clusters):
      for i in range(current_nb_clusters - nb_clusters):
        self.clusterCenterList.pop(i)




