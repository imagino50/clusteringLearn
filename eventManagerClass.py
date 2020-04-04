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
        self.eventList_previous = []
        self.clusterer_previous = None

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
    def clusterEvents(self, min_cluster_size):
      if (len(self.eventList) > min_cluster_size):
        clusterer = Clustering.detectCluster(self.eventList, min_cluster_size)

        matchingClustersDict = {}
        if (self.clusterer_previous is not None) and (clusterer.labels_[clusterer.labels_ != -1].size > 0 ):
          matchingClustersDict = self.correlateClusters(clusterer.labels_)

        if(len(matchingClustersDict) > 0):
          for event, label, probabilities in zip(self.eventList, clusterer.labels_, clusterer.probabilities_):
            event.setClustererProbabilities(probabilities)
            if(label == -1):
              event.setCluster(-1)
            else:
              clusterId = matchingClustersDict[label]
              event.setCluster(clusterId)
             
        elif len(clusterer.labels_ > 0):
          for event, label, probabilities in zip(self.eventList, clusterer.labels_, clusterer.probabilities_):
            event.setCluster(label)
            event.setClustererProbabilities(probabilities)

        self.clusterer_previous = clusterer
        self.eventList_previous = self.eventList


  # =============================================================================
  # Clustering Correlation between previous and current clusters
  # =============================================================================
    def correlateClusters(self, labels):
      matchingClustersDict = {}
      for cur_idx in range(len(self.eventList)):
        cur_clusterId = labels[cur_idx]
        if cur_clusterId != -1:
           for prev_idx in range(len(self.eventList_previous)):
              prev_clusterId = self.eventList_previous[prev_idx].clusterId
              if(self.eventList[cur_idx].x == self.eventList_previous[prev_idx].x and
              self.eventList[cur_idx].y == self.eventList_previous[prev_idx].y and
              prev_clusterId != -1):
                if prev_clusterId not in matchingClustersDict.values():
                  matchingClustersDict[cur_clusterId] = prev_clusterId
                  #print(u"FOUND! cur_clusterId:", cur_clusterId , '  prev_clusterId:', prev_clusterId)
                  break

      # Current cLusters that ccannot be match with previous clusters
      clusterIdMax = np.amax(labels) + 1 #clusterer.labels_.max()
      for cluster_id in range(clusterIdMax):
        if cluster_id not in matchingClustersDict:
          i = 0
          while i in matchingClustersDict.values():
            i = i + 1
          matchingClustersDict[cluster_id] = i

      return matchingClustersDict


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
