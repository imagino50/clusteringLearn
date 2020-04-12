# Module imports
import clusterClass as Cluster

# Third party imports


class ClusterManagerClass:
    # =============================================================================
    # __init__() functions as the class constructor
    # =============================================================================
    def __init__(self):
      self.clusterList = []


  # =============================================================================
  # Create a cluster
  # =============================================================================
    def createCluster(self, clusterId, exemplar, persistence):
      cluster = Cluster.ClusterClass(clusterId, exemplar, persistence)
      self.clusterList.append(cluster)


  # =============================================================================
  # Update existing clusters
  # =============================================================================
    def updateCluster(self, clusterId, exemplar, persistence):
        for cluster in self.clusterList:
          if cluster.Id == clusterId:
            cluster.update(exemplar, persistence)
            break


  # =============================================================================
  # Update existing clusters
  # =============================================================================
    def updateClusters(self, matchingClustersDict, exemplars, persistences):
      for index, (exemplar, persistence) in enumerate(zip(exemplars, persistences)):
        clusterId = matchingClustersDict[index]
        #if any(cluster.clusterId == clusterId for cluster in self.clusterList):
        #next((cluster for cluster in self.clusterList if cluster.clusterId == clusterId), None)
        for cluster in self.clusterList:
          if cluster.Id == clusterId:
            cluster.update(exemplar, persistence)
            break
  
  # =============================================================================*/
  # Remove Cluster(s) if they are not anymore in the dictionary
  # =============================================================================*/
    def removeDeadClusters(self, matchingClustersDict):
      #lenBefore = len(self.clusterList)
      self.clusterList = [cluster for cluster in self.clusterList if cluster.Id in matchingClustersDict.values()]
      #lenAfter = len(self.clusterList)
      #if lenBefore != lenAfter:
      #  print(u"removeDeadClusters len(self.clusterList) before:",lenBefore)
      #  print(u"removeDeadClusters len(self.clusterList) after:",lenAfter)


  # =============================================================================*/
  # Remove all Clusters
  # =============================================================================*/
    def removeAllClusters(self):
      self.clusterList.clear()


  # =============================================================================*/
  # Return ClusterList
  # =============================================================================*/
    def getClusterList(self):
      return self.clusterList


  # =============================================================================*/
  # Return data to plot persistence
  # =============================================================================*/
    def getDataToPlot(self, roundPersistence, lifeTimeFilter):
      IdList = []
      lifeTimeList = []
      persistenceList = []

      if len(self.clusterList) > 0:
        clusterListFiltered = [cluster for cluster in self.clusterList if cluster.lifeTime > lifeTimeFilter]
        if len(clusterListFiltered) > 0:
          IdList, lifeTimeList, persistenceList = map(list, zip(*((c.Id, c.lifeTime, round(c.currentPersistence, roundPersistence))
                      for c in clusterListFiltered)))

      return IdList, lifeTimeList, persistenceList


  # =============================================================================*/
  # Print 
  # =============================================================================*/
    def printClusters(self):
      for cluster in self.clusterList:
        print(u"clusterId: ", cluster.Id, " lifeTime:", cluster.lifeTime, " exemplarHisto:", cluster.exemplarHisto, " persistenceHisto:", cluster.persistenceHisto)

