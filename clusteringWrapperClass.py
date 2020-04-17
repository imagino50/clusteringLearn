# Module imports
import clustering as Clustering
import clusterManagerClass as ClusterManager
import utils as utils

# Third party imports

  

class ClusteringWrapperClass:
    # =============================================================================
    # __init__() functions as the class constructor
    # =============================================================================
    def __init__(self):
        self.clusterMng = ClusterManager.ClusterManagerClass()


    # =============================================================================
    # Main function : Cluster Events
    # =============================================================================
    def clusterEvents(self, eventList, min_cluster_size, previousLabelsSize, fisrtClustering):
        clusterer = Clustering.detectCluster(eventList, min_cluster_size)

        matchingClustersDict = {}
        if (not fisrtClustering): 
            matchingClustersDict = self.__detectMatchClusters(eventList, clusterer.labels_, clusterer.exemplars_, clusterer.cluster_persistence_, previousLabelsSize)
            self.clusterMng.removeDeadClusters(matchingClustersDict)
            matchingClustersDict = self.__detectNewClusters(matchingClustersDict, clusterer.labels_.max() + 1, clusterer.exemplars_, clusterer.labels_)

        return clusterer, matchingClustersDict


    # =============================================================================
    # Compute cluster matching between previous and current clusters
    # =============================================================================
    def __detectMatchClusters(self, eventList, labels, exemplars, cluster_persistence, previousLabelsSize):
        matchingClustersDict = {}

        idxClusters = sorted(range(len(cluster_persistence)), key=lambda k: cluster_persistence[k], reverse=True)
        for idx in idxClusters:
            for event, label in zip(eventList, labels):
                if (event.clusterId != -1) and (label == idx):
                    isStillExemplar = utils.isCoordinatesMatch(event, exemplars[label])
                    if (event.clusterId not in matchingClustersDict.values()) and isStillExemplar and event.clusterExemplar:
                        matchingClustersDict[label] = event.clusterId
                        self.clusterMng.updateCluster(event.clusterId, exemplars[label], cluster_persistence[label])
                        break
                        #print(u"FOUND! cur_clusterId:", label , '  prev_clusterId:', event.clusterId)
                        #print(u"FOUND! event.x :", event.x  , '  event.y:', event.y)

        sizeDict = len(matchingClustersDict) 
        if (sizeDict< previousLabelsSize) and (sizeDict < labels.max() +1):
            for event, label in zip(eventList, labels):
                if (event.clusterId != -1) and (label != -1):
                    if (label not in matchingClustersDict) and (event.clusterId not in matchingClustersDict.values()):
                        matchingClustersDict[label] = event.clusterId
                        self.clusterMng.updateCluster(event.clusterId, exemplars[label], cluster_persistence[label])
                        print(u"FOUND! cur_clusterId:", label , '  prev_clusterId:', event.clusterId)
                        
        return matchingClustersDict


    # =============================================================================
    # Compute current clusters that cannot be match with previous clusters
    # =============================================================================
    def __detectNewClusters(self, matchingClustersDict, clusterIdMax,  exemplars, cluster_persistence):
        for clusterId in range(clusterIdMax):
            if clusterId not in matchingClustersDict:
                i = 0
                while i in matchingClustersDict.values():
                    i = i + 1
                matchingClustersDict[clusterId] = i
                self.clusterMng.createCluster(i, exemplars[clusterId], cluster_persistence[clusterId])
                print(u"createCluster! clusterId:", i )
                #print(matchingClustersDict)

        return matchingClustersDict


    # =============================================================================
    # Get data to plot persistence
    # =============================================================================
    def getDataToPlot(self, roundPersistence, lifeTimeFilter):
        return self.clusterMng.getDataToPlot(roundPersistence, lifeTimeFilter)
