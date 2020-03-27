# Module imports

# Third party imports
import numpy as np
import pandas as pd
import collections


class EventClass(object):
# =============================================================================
# __init__() functions as the class constructor
# =============================================================================
    def __init__(self, center_x, center_y, centerIntensity):
        self.x = center_x
        self.y = center_y
        self.intensity = centerIntensity
        self.radius = 0
        self.clusterId = -1

# =============================================================================
# update Event shape
# =============================================================================
    def updateShape(self, incRadius, incIntensity):
        # decrease the intensity
        self.intensity -= incIntensity

        # increase the radius
        self.radius += incRadius
  
# =============================================================================
# set Event's cluster
# =============================================================================
    def setCluster(self, id):
        self.clusterId = id


  

