# Module imports

# Third party imports


class EventClass:
# =============================================================================
# __init__() functions as the class constructor
# =============================================================================
    def __init__(self, center_x, center_y, centerIntensity):
        self.x = center_x
        self.y = center_y
        self.intensity = centerIntensity
        self.clustererProbability = 0
        self.clusterExemplar = False
        self.radius = 0
        self.clusterId = -1


# =============================================================================
# Update Event shape
# =============================================================================
    def updateShape(self, incRadius, incIntensity):
        # decrease the intensity
        self.intensity -= incIntensity

        # increase the radius
        self.radius += incRadius
  
  
# =============================================================================
# set Event clustererProbability
# =============================================================================
    def setClustererProbability(self, clustererProbability):
        self.clustererProbability = clustererProbability


# =============================================================================
# set Event clusterExamplar
# =============================================================================
    def setClusterExemplar(self, clusterExemplar):
        self.clusterExemplar = clusterExemplar


# =============================================================================
# set Event's cluster
# =============================================================================
    def setCluster(self, id):
        self.clusterId = id


  

