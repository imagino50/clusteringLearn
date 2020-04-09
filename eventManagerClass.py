# Module imports
import eventClass as Event
import clustering as Clustering

# Third party imports
import numpy as np
import seaborn as sns
#import scipy.spatial as spatial

class EventManagerClass:
    # =============================================================================
    # __init__() functions as the class constructor
    # =============================================================================
    def __init__(self):
        self.eventList = []
        self.fisrtClustering = True

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
  # Clustering Events
  # =============================================================================
    def clusterEvents(self, min_cluster_size, min_proba_cluster):
      if (len(self.eventList) > min_cluster_size):
        clusterer = Clustering.detectCluster(self.eventList, min_cluster_size)
        #self.printEvents()
        #print(clusterer.labels_)

        matchingClustersDict = {}
        if (self.fisrtClustering == False) and (clusterer.labels_[clusterer.labels_ != -1].size > 0 ):
          matchingClustersDict = self.matchClusters(clusterer.labels_, clusterer.exemplars_)
          #print(matchingClustersDict)

        if len(matchingClustersDict) > 0:
          for event, label, probability in zip(self.eventList, clusterer.labels_, clusterer.probabilities_):
            event.setClustererProbability(probability)
            if (label == -1) or (probability < min_proba_cluster):
              event.setCluster(-1)
              event.setClusterExemplar(False)
            else:
              clusterId = matchingClustersDict[label]
              event.setCluster(clusterId)
              event.setClusterExemplar(self.isCoordinatesMatch(event, clusterer.exemplars_[label]))
        elif len(clusterer.labels_ > 0):
          for event, label, probability in zip(self.eventList, clusterer.labels_, clusterer.probabilities_):
            event.setClustererProbability(probability)
            if (label == -1) or (probability < min_proba_cluster):
              event.setCluster(-1)
              event.setClusterExemplar(False)
            else:
              event.setCluster(label)
              event.setClusterExemplar(self.isCoordinatesMatch(event, clusterer.exemplars_[label]))

        self.fisrtClustering = False


  # =============================================================================
  # Clustering Correlation between previous and current clusters
  # =============================================================================
    def matchClusters(self, labels, exemplars):
      matchingClustersDict = {}
      for event, label in zip(self.eventList, labels):
         isStillExemplar = self.isCoordinatesMatch(event, exemplars[label])
         if (event.clusterId != -1) and (label != -1) and event.clusterExemplar  and isStillExemplar:
          if event.clusterId not in matchingClustersDict.values():
            matchingClustersDict[label] = event.clusterId
            #print(u"FOUND! cur_clusterId:", label , '  prev_clusterId:', event.clusterId)
            #print(u"FOUND! event.x :", event.x  , '  event.y:', event.y)

      # Current cLusters that cannot be match with previous clusters
      clusterIdMax = np.amax(labels) + 1 #clusterer.labels_.max()
      for cluster_id in range(clusterIdMax):
        if cluster_id not in matchingClustersDict:
          i = 0
          while i in matchingClustersDict.values():
            i = i + 1
          matchingClustersDict[cluster_id] = i

      return matchingClustersDict


  # =============================================================================
  # Return true if the Event coordinates match one of the array of coordinates
  # =============================================================================
    def isCoordinatesMatch(self, event, exemplars):
      coordinates = np.array([event.x, event.y])
      return any(np.array_equal(exemplar, coordinates) for exemplar in exemplars)


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
  # Return EventList
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


  # =============================================================================*/
  # Print EventList
  # =============================================================================*/
    def printEvents(self):
      for item in self.eventList:
        print(u"x:", item.x, '  y:', item.y, "  clusterId: ", item.clusterId)

