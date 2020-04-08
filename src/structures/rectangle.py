from src.structures.point import Point
from src.utils import is_monotic3

class SimpleRectangle():
    def __init__(self, x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.p1 = Point(x,y)                # top left corner
        self.p2 = Point(x+w-1,y+h-1)        # bottom right corner

    def __str__(self):
        output = '[{}, {}, {}, {}]'.format(self.x, self.y, self.w, self.h)
        return output

    def contains_rect(self, targetRect):
        '''
        returns true if targetRect is inside this rectangle
        '''

        # if both points (p1,p2) of targetRect are inside this rect, 
        # then whole targetRect is inside this rect
        output = self.contains_point(targetRect.p1) and self.contains_point(targetRect.p2)
        return output

    def contains_point(self, targetPoint):
        '''
        returns true if targetPoint is inside this rectangle
        '''

        # check if target point lies between vertical sides of rectangle
        flag1 = is_monotic3(self.p1.x, targetPoint.x, self.p2.x)

        # check if target point lies between horizontal sides of rectangle
        flag2 = is_monotic3(self.p1.y, targetPoint.y, self.p2.y)

        # if targetPoint lies between both sides, then it is inside the rectangle 
        output = flag1 and flag2

        return output

    def get_area(self):
        '''
        returns area of rectangle
        '''
        area = self.w * self.h
        return area

