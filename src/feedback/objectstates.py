from enum import Enum

class ObjectState(Enum):
    UNKNOWN = 0
    OUTSIDE_CANVAS = 1
    OUTSIDE_ROI = 2
    CROSSING_ROI = 3
    INSIDE_ROI = 4
        


