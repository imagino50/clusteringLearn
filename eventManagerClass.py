# Module imports
import eventClass as Event

# Third party imports
import numpy as np
import pandas as pd
import collections


class EventManagerClass(object):
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
        x,y,sizeList,intensityList  = map(list, zip( *((e.x, e.y, e.radius, e.intensity) for e in self.eventList)) )
        offsetList = [list(x) for x in zip(x, y)]   
        return offsetList, sizeList, intensityList




