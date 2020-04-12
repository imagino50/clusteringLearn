# Module imports
import eventClass as Event
import clusteringWrapperClass as ClusteringWrapper
import utils as utils

# Third party imports
import numpy as np
import seaborn as sns


class EventManagerClass:
    # =============================================================================
    # __init__() functions as the class constructor
    # =============================================================================
    def __init__(self):
        self.eventList = []
        self.fisrtClustering = True
        self.previousLabelsSize = 0
        self.clusteringWrapper = ClusteringWrapper.ClusteringWrapperClass()

        sns.set_color_codes()
        # https://seaborn.pydata.org/tutorial/color_palettes.html
        color_palette = sns.color_palette('bright') #deep
        self.r =  [x[0] for x in color_palette]
        self.g =  [x[1] for x in color_palette]
        self.b =  [x[2] for x in color_palette]
        #print(color_palette)


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
  # Cluster Eventsusing HDBSCAN
  # =============================================================================
    def clusterEvents(self, min_cluster_size, min_proba_cluster):
      if (len(self.eventList) > min_cluster_size):

        clusterer, matchingClustersDict = self.clusteringWrapper.clusterEvents(
          self.eventList, 
          min_cluster_size, 
          min_proba_cluster, 
          self.previousLabelsSize, 
          self.fisrtClustering)
        
        for event, label, probability in zip(self.eventList, clusterer.labels_, clusterer.probabilities_):
          event.setClustererProbability(probability)
          if (label == -1) or (probability < min_proba_cluster):
            event.setCluster(-1)
            event.setClusterExemplar(False)
          else:
            if len(matchingClustersDict) > 0:
              clusterId = matchingClustersDict[label]
            else:
              clusterId = label
            event.setCluster(clusterId)
            event.setClusterExemplar(utils.isCoordinatesMatch(event, clusterer.exemplars_[label]))
       
        self.fisrtClustering = False
        self.previousLabelsSize = clusterer.labels_.max() +1


  # =============================================================================
  # Remove Events with intensity lower than intensityMin
  # =============================================================================
    def removeWeakEvents(self, intensityMin):
        self.eventList=[
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
  # Return data to Scatter events
  # =============================================================================*/
    def getDataToScatter(self, centerIntensity, intensityMin):
        x, y, sizeList = map(list, zip(*((e.x, e.y, e.radius)
                           for e in self.eventList)))

        offsetList=[list(x) for x in zip(x, y)]

        r1 = [self.r[event.clusterId] if event.clusterId >= 0 else 0.0 for event in self.eventList]
        g1 = [self.g[event.clusterId] if event.clusterId >= 0 else 0.0 for event in self.eventList]
        b1 = [self.b[event.clusterId] if event.clusterId >= 0 else 0.0 for event in self.eventList]
        a = [(event.intensity - intensityMin)/(centerIntensity - intensityMin) for event in self.eventList]
        cluster_colors = tuple(zip(r1, g1, b1, a))

        #cluster_member_colors = [sns.desaturate(x, p) for x, p in zip(cluster_colors, clusterer.probabilities_)]
        return offsetList, sizeList, cluster_colors


  # =============================================================================
  # Return data to plot cluster persistence
  # =============================================================================
    def getDataToPlot(self, roundPersistence, lifeTimeFilter):
      IdList, lifeTimeList, persistenceList = self.clusteringWrapper.getDataToPlot(roundPersistence, lifeTimeFilter)
      r1 = [self.r[id] for id in IdList]
      g1 = [self.g[id] for id in IdList]
      b1 = [self.b[id] for id in IdList]
      a = [1] * len(IdList)
      cluster_colors = tuple(zip(r1, g1, b1, a))

      return IdList, lifeTimeList, persistenceList, cluster_colors


  # =============================================================================*/
  # Print EventList
  # =============================================================================*/
    def printEvents(self):
      for item in self.eventList:
        print(u"x:", item.x, '  y:', item.y, "  clusterId: ", item.clusterId)

