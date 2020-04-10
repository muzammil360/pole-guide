from src.structures.rectangle import SimpleRectangle
from src.feedback.feedbacktypes import FeedbackTypes
from src.feedback.objectstates import ObjectState
from src.utils import iou
from src.logger import get_logger 

def applyGuard(canvas, guard):
    '''
    returns a new SimpleRectangle with guard applied on canvas
    '''
    x = canvas.x + guard
    y = canvas.y + guard
    w = canvas.w - 2*guard
    h = canvas.h - 2*guard

    output = SimpleRectangle(x,y,w,h)

    return output



class ZoomFeedback():
    def __init__(self, canvas,guard = 0, iouThresLower = 0.3 , iouThresHigher = 7.0):
        '''
        initializes ZoomFeedback object

        canvas:         simple rectangle representing the image canvas
        guard:          no. of pixels acting as guard band from all 4 sides
        '''
        self.canvas = canvas
        self.guard = guard
        self.iouThresLower = iouThresLower
        self.iouThresHigher = iouThresHigher

        self.logger = get_logger('ZoomFeedback')

        self.roi = applyGuard(self.canvas, self.guard)      # get Region of Interest (ROI)


    def run(self, detection):
        '''
        applies feedback algorithm on detection
        '''

        self.logger.debug('canvas.iou: {}'.format(iou(self.canvas, detection)))
        self.logger.debug('roi.iou: {}'.format(iou(self.roi, detection)))

        containsDet = self.roi.contains_rect(detection)
        self.logger.debug('roi.contains_rect: {}'.format(containsDet))
        self.logger.debug('roi.contains_rect: {}'.format(type(containsDet)))

         # compute object state
        state = self.get_object_state(detection)
        self.logger.debug('current object state: {}'.format(state))

        # return feedback based on state
        feedback = self.determine_feedback(detection, state)
        self.logger.debug('current feedback state: {}'.format(feedback))


        return feedback 

    def get_object_state(self,detection):
        '''
        detects the state of object returns a valid value of enum ObjectState
        '''
 
        if iou(self.canvas,detection) == 0:
            return ObjectState.OUTSIDE_CANVAS
        elif iou(self.roi, detection) ==0:
            return ObjectState.OUTSIDE_ROI


        if int(self.roi.contains_rect(detection)) == 1:
            return ObjectState.INSIDE_ROI
        else:
            return ObjectState.CROSSING_ROI


    def determine_feedback(self, detection, state):
        '''
        proposes an appropriate feedback based on object state and detection position
        '''

        feedback = None

        if state == ObjectState.UNKNOWN:
            feedback = FeedbackTypes.SORRY

        elif state ==ObjectState.OUTSIDE_CANVAS:
            # we don't handle this case
            feedback = FeedbackTypes.SORRY

        elif state == ObjectState.OUTSIDE_ROI:
            # we don't handle this case
            feedback = FeedbackTypes.SORRY

        elif state == ObjectState.CROSSING_ROI:
            # we don't handle this case
            feedback = FeedbackTypes.SORRY

        elif state == ObjectState.INSIDE_ROI:
            feedback = self.handle_inside_roi_case(detection)
        
        else:
            feedback = FeedbackTypes.SORRY

        return feedback


    def handle_inside_roi_case(self,detection):
        '''
        proposes an appropriate feedback for `ObjectState.INSIDE_ROI` case
        '''

        iouScore = iou(self.roi, detection)
        output = None

        if iouScore < self.iouThresLower:
            output = FeedbackTypes.ZOOM_IN
        elif iouScore > self.iouThresHigher: 
            output = FeedbackTypes.ZOOM_OUT
        else:
            output = FeedbackTypes.STABLE

        return output
