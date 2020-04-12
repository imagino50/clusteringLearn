# Module imports
from collections import deque

# Third party imports


class ClusterClass:
# =============================================================================
# __init__() functions as the class constructor
# =============================================================================
    def __init__(self, clusterId, exemplar, persistence):
        self.Id = clusterId
        #self.exemplarHisto = deque(maxlen=3)
        #self.exemplarHisto.append(exemplar)
        self.currentPersistence = persistence
        #self.persistenceHisto = deque(maxlen=5)
        #self.persistenceHisto.append(persistence)
        self.lifeTime = 0


# =============================================================================
# set clusterId
# =============================================================================
    def setClusterId(self, clusterId):
        self.Id = clusterId


# =============================================================================
# Update Cluster 
# =============================================================================
    def update(self, exemplar, persistence):
        self.increaseLifeTime()
        self.currentPersistence = persistence
        #self.storeExemplar(exemplar)
        #self.storePersistence(persistence)


# =============================================================================
# Increase Cluster lifeTime
# =============================================================================
    def increaseLifeTime(self):
        self.lifeTime += 1


# =============================================================================
# store cluster persistence into historic
# =============================================================================
    #def storePersistence(self, persistence):
    #    self.persistenceHisto.append(persistence)


# =============================================================================
# store cluster exemplar into historic
# =============================================================================
    #def storeExemplar(self, exemplar):
    #    self.exemplarHisto.append(exemplar)
  

# =============================================================================
# Deleting (Calling destructor) 
# =============================================================================
    #def __del__(self): 
        #print('Destructor called, ClusterClass deleted.') 
        #self.exemplarHisto.clear()
        #self.persistenceHisto.clear()