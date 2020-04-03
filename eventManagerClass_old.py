# Module imports
import eventClass as Event
import clustering as Clustering

# Third party imports
import numpy as np
import pandas as pd
import collections
import scipy.spatial as spatial


class EventManagerClass:
    # =============================================================================
    # __init__() functions as the class constructor
    # =============================================================================
    def __init__(self):
        self.eventList = []
        self.clusterer = []
        self.previousEventDataFrame = pd.DataFrame()


  # =============================================================================*/
  # Add Event
  # =============================================================================*/
    def addEvent(self, event):
        self.eventList.append(event)

  # =============================================================================*/
  # Add new Event at position (x,y)
  # =============================================================================*/
    def createEvent(self, x, y, centerIntensity):
        self.eventList.append(
            Event.EventClass(round(x), round(y), centerIntensity)
        )

  # =============================================================================
  # Update Events shape
  # =============================================================================
    def updateEventsShape(self, incRadius, incIntensity):
        # loop over each event to update it
        for event in self.eventList:
            event.updateShape(incRadius, incIntensity)

  # =============================================================================
  # Set Events propagatedIntensity
  # =============================================================================
    # def setEventsPropagatedIntensity(self, distance):
    # https://stackoverflow.com/questions/32424604/find-all-nearest-neighbors-within-a-specific-distance
    #    point_tree = spatial.cKDTree(self.eventList)
    #    # loop over each event to calulate each propagatedIntensity
    #    for event in self.eventList:
    #        # This finds the index of all points within distance "distance" of [event.x, event.y].
    #        point_tree.query_ball_point([event.x, event.y], distance))
    #        propagatedIntensity =
    #        event.setPropagatedIntensity(propagatedIntensity)

  # =============================================================================
  # Clustering Events
  # =============================================================================
    def clusterEvents(self):
      if (len(self.eventList) > 3):
        # https://stackoverflow.com/questions/34997174/how-to-convert-list-of-model-objects-to-pandas-dataframe
        currentEventDataFrame = pd.DataFrame(columns=['x','y'])
        x, y = map(list, zip(*((e.x, e.y) for e in self.eventList)))
        coordinatesList = [list(el) for el in zip(x, y)]
        currentEventDataFrame = pd.DataFrame(coordinatesList, columns=['x','y'])

        clusterer = Clustering.detectCluster(currentEventDataFrame)

        currentEventDataFrame['clusterId'] = clusterer.labels_
        print(clusterer.labels_)
        
        # Exclde noise & Group by clusterId
        currentEventDataFrame = currentEventDataFrame[currentEventDataFrame.clusterId != -1].groupby(['clusterId'])  

        #print("currentEventDataFrame")
        #for key, item in currentEventDataFrame:
        #  print(currentEventDataFrame.get_group(key), "\n\n")

        correlationDataFrame = pd.DataFrame(columns=['current_cluster','previous_cluster', 'nbCommonsCoordinates'])
        if (self.previousEventDataFrame.size != 0):
          correlationDataFrame = self.clusterCorrelation(currentEventDataFrame)
          #print("correlationDataFrame")
          #print(correlationDataFrame)

        if(correlationDataFrame.empty):
          for event, label in zip(self.eventList, clusterer.labels_):
              event.setCluster(label)
        else:
            matchingDict = self.clusterMatching(correlationDataFrame, len(currentEventDataFrame.groups.keys()))
            print(matchingDict)
            for event, label in zip(self.eventList, clusterer.labels_):
              if(label == -1):
                event.setCluster(-1)
              else:
                clusterId = matchingDict[label]
                event.setCluster(clusterId)

        self.previousEventDataFrame = currentEventDataFrame


  # =============================================================================
  # Clustering Correlation between previous and current clusters
  # =============================================================================
    def clusterCorrelation(self, currentEventDataFrame):
        # Init matrix correlation between previous and current clusters
        nbRows = len(currentEventDataFrame.groups.keys())
        NbColums = len(self.previousEventDataFrame.groups.keys())
        correlationDataFrame = pd.DataFrame(columns=['current_cluster','previous_cluster', 'nbCommonsCoordinates'])

        # Fill matrix correlation
        for current_cluster_id in range(nbRows):
          #for key, item in currentEventDataFrame:
          #  print(currentEventDataFrame.get_group(key), "\n\n")
          for previous_cluster_id in range(NbColums):
            #for key, item in self.previousEventDataFrame:
            #  print(self.previousEventDataFrame.get_group(key), "\n\n")
            df_current = currentEventDataFrame.get_group(current_cluster_id)
            df_previous = self.previousEventDataFrame.get_group(previous_cluster_id)
            nbCommonsCoordinates = len(pd.merge(df_current, df_previous, how='inner', on=['x','y']).index)
            if(nbCommonsCoordinates > 0):
              new_row = {'current_cluster':current_cluster_id, 
              'previous_cluster':previous_cluster_id, 
              'nbCommonsCoordinates':nbCommonsCoordinates}
              correlationDataFrame = correlationDataFrame.append(new_row, ignore_index=True)
        correlationDataFrame.sort_values(["nbCommonsCoordinates", "current_cluster"], ascending=False, inplace=True)

        return correlationDataFrame

  # =============================================================================
  # Select Previous Clustering matching to current Clustering using CorrelationDataFrame 
  # =============================================================================
    def clusterMatching(self, correlationDataFrame, nbCurrentCluster):
      matchingDict = {} 
      while(correlationDataFrame.size > 0): # infinite loop
        current_cluster_id = correlationDataFrame['current_cluster'].iloc[0]
        previous_cluster_id = correlationDataFrame['previous_cluster'].iloc[0]
        matchingDict[current_cluster_id] = previous_cluster_id

         # Remove first row
        correlationDataFrame = correlationDataFrame.iloc[1:]

        # Remove rows with this current_cluster_id or this previous_cluster_id
        correlationDataFrame = correlationDataFrame[(correlationDataFrame['current_cluster']  != current_cluster_id)] 
        correlationDataFrame = correlationDataFrame[(correlationDataFrame['previous_cluster'] != previous_cluster_id)]

        #print("correlationDataFrame2")
        #print(correlationDataFrame)
      #print("matchingDict:_before")
      #print(matchingDict)
      for cluster_id in range(nbCurrentCluster):
        if(cluster_id not in matchingDict): 
          i = 0
          while i in matchingDict.values():
            i = i + 1
          matchingDict[cluster_id] = i
    
      return matchingDict


  # =============================================================================
  # Remove Events with intensity lower than intensityMin
  # =============================================================================
    def removeWeakEvents(self, intensityMin):
        self.eventList = [
            item for item in self.eventList if item.intensity > intensityMin]

  # =============================================================================*/
  # Remove all Events
  # =============================================================================*/
    def removeAllEvents(self):
        self.eventList.clear()

  # =============================================================================*/
  # Return EventList
  # =============================================================================*/
    def getEventList(self):
        return self.eventList

  # =============================================================================*/
  # Return EventList
  # =============================================================================*/
    def getDataToScatter(self):
        x, y, sizeList = map(list, zip(*((e.x, e.y, e.radius) for e in self.eventList)))
        offsetList = [list(x) for x in zip(x, y)]
        return offsetList, sizeList

  # =============================================================================*/
  # Print EventList
  # =============================================================================*/
    def printEvents(self):
      for item in self.eventList:
        print(u"x:", item.x , '  y:', item.y, "  clusterId: ", item.clusterId)
 
