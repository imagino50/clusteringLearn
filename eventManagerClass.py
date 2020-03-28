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
      if(len(self.eventList) > 3):
        #https://stackoverflow.com/questions/34997174/how-to-convert-list-of-model-objects-to-pandas-dataframe
        x, y = map(list, zip(*((e.x, e.y) for e in self.eventList)))
        offsetList = [list(el) for el in zip(x, y)]
        inputDataFrame = pd.DataFrame(offsetList, columns=['x', 'y'])

        clusterer = Clustering.detectCluster(inputDataFrame)

        for event, label in zip(self.eventList, clusterer.labels_):
            event.setCluster(label)


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

