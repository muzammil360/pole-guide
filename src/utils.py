

def iou(rect1, rect2):
    '''
    computes Intersection Over Union (IOU) of two rectangles
    # NOTES:
    iou reference: https://www.pyimagesearch.com/2016/11/07/intersection-over-union-iou-for-object-detection/
    https://gist.github.com/meyerjo/dd3533edc97c81258898f60d8978eddc
    '''
    # TODO: implement the method

    iouScore = -1

    # determine the coordinates of intersecting rectangle
    x1 = max(rect1.p1.x, rect2.p1.x)
    x2 = min(rect1.p2.x, rect2.p2.x)
    y1 = max(rect1.p1.y, rect2.p1.y)
    y2 = min(rect1.p2.y, rect2.p2.y)

    w = max(x2 - x1 +1, 0)
    h = max(y2 - y1 +1, 0)
    inter_area = w*h

    # if intersecting rectangle area is zero, iou is automatically zero
    if inter_area == 0:
        return 0                

    # get individual rectangle areas
    rect1Area = rect1.get_area()
    rect2Area = rect2.get_area()

    # compute iou
    iouScore = inter_area/float(rect1Area + rect2Area - inter_area)

    
    return iouScore


def is_monotic3(a,b,c):
    '''
    returns true if a<=b<=c
    '''
    output = (a<=b) and (b<=c)

    return output