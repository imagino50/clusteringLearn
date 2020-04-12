# Third party imports
import numpy as np

# =============================================================================
# Return true if the Event coordinates match one of the array of coordinates
# =============================================================================
def isCoordinatesMatch(event, exemplars):
    coordinates = np.array([event.x, event.y])
    return any(np.array_equal(exemplar, coordinates) for exemplar in exemplars)