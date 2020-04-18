import sys
import argparse
import os

import cv2

from src.logger import get_logger
from src.sensors.camera import Camera
from src.structures.rectangle import SimpleRectangle
from src.detectors.yolov3 import Yolov3
from src.feedback.zoomfeedback import ZoomFeedback
from src.feedback.feedbacktypes import FeedbackTypes
from src.utils import rectify_detection

logger = get_logger('Main')

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--guard_size',type=int, default = 5, required= False, help='no. of pixels acting as guard band inside image')
    parser.add_argument('--iou_thres_lower',type=float, default = 0.3 , required= False, help='minimum iou detection should have with image')
    parser.add_argument('--iou_thres_higher',type=float, default = 0.5 , required= False, help='maximum iou detection should have with image')
    parser.add_argument('--weights',type=str , required= True, help='path to weights file')
    parser.add_argument('--config',type=str , default = 'data/xyolov3-tiny-obj.cfg' ,required= False, help='path to weights file')
    parser.add_argument('--visualize', default=False, required= False, action='store_true', help='show yolo output?')
    parser.add_argument('--detection_conf', type=float, default = 0.4 , required= False, help='yolo detection threshold')
    
    args = parser.parse_args()
    return args

# This function is for testing only. 
# Don't change it unless you know it 
def get_feedback_test_data():
    '''
    returns synthetic test data for Feedback object
    '''
    canvasWidth = 110;
    canvasHeight = 110;

    canvas = SimpleRectangle(0,0,canvasWidth, canvasHeight)


    detections = []         # list of simple rects

    for k in range(3,110,2):
        w = k
        h = k    
        x = int(canvasWidth/2 - w/2)
        y = int(canvasHeight/2 - h/2)

        r = SimpleRectangle(x,y,w,h)
        detections.append(r)

    return canvas, detections


# This function is for testing only. 
# Don't change it unless you know it 
def evaluate_detector_visually():
    '''
    evaluates yolo detector visually by visualizing detections
    '''
    dataset = r'/media/muzammil/Data/datasets/muhammad-a--detection-system--when-to-take-image/dataset3/eval'
    filelist = os.listdir(dataset)


    # make detector
    config_addr = 'data/xyolov3-tiny-obj.cfg' 
    weights_addr = './../weights/xyolov3-tiny-1400.weights' 
    input_dim = 416 
    confidence = 0.25
    num_classes = 1
    nms_theshold = 0.4
    class_name_fileaddr = 'data/obj.names'
    color_pallete_fileaddr = 'data/pallete'
    visualize_output = True 
    
    det = Yolov3(config_addr, 
        weights_addr, 
        input_dim, 
        confidence, 
        num_classes, 
        nms_theshold,
        class_name_fileaddr,
        color_pallete_fileaddr,
        visualize_output)

    for file in filelist:
        filepath = os.path.join(dataset,file)
        
        # read image
        img = cv2.imread(filepath)

        # apply detector
        img = cv2.resize(img,(600,400))
        detections = det.detect(img)

        # visualize
        # cv2.imshow('img',img)
        print(file)
        print(detections)
        print('='*10)

        # wait
        cv2.waitKey(int(1000))

    sys.exit(0)
    return 

# This function is for testing only. 
# Don't change it unless you know it 
def camera_test():
    cam = Camera(0)

    while (1):

        img = cam.getReading()
        cv2.imshow('img',img)
        cv2.waitKey(int(1000/25))

    return


if __name__ == '__main__':

    # evaluate_detector_visually()

    args = parse_args()
    logger.info(args)

    # make camera
    cam = Camera(0)
    img = cam.getReading()

    # make detector
    config_addr = args.config 
    weights_addr = args.weights 
    input_dim = 416 
    confidence = args.detection_conf
    num_classes = 1
    nms_theshold = 0.4
    class_name_fileaddr = 'data/obj.names'
    color_pallete_fileaddr = 'data/pallete'
    visualize_output = args.visualize 
    
    det = Yolov3(config_addr, 
        weights_addr, 
        input_dim, 
        confidence, 
        num_classes, 
        nms_theshold,
        class_name_fileaddr,
        color_pallete_fileaddr,
        visualize_output)


    # make feedback processor
    guard = args.guard_size
    thres_lower = args.iou_thres_lower
    thres_higher = args.iou_thres_higher
    canvas = SimpleRectangle(0,0,img.shape[1], img.shape[0])
    logger.debug('making canvas: {}'.format(canvas))

    feedbackProcessor = ZoomFeedback(canvas, guard, thres_lower, thres_higher)


    while True:
        try:
            # read image
            img = cam.getReading()
            logger.info('FPS: {:.4f}'.format(cam.getCurrFPS()))

            # get detections
            detections = det.detect(img)
            logger.debug('{}'.format(detections.shape))
            if len(detections) == 0:
                continue

            # apply feedback processor
            x = detections[0][1]
            y = detections[0][2]
            w = detections[0][3] - detections[0][1] + 1
            h = detections[0][4] - detections[0][2] + 1
            detections = SimpleRectangle(x,y,w,h)
            logger.debug('detection rect: {}'.format(detections))

            detections = rectify_detection(detections, canvas, 1)
            logger.debug('rectified detection rect: {}'.format(detections))

            fb = feedbackProcessor.run(detections)

            # print the feedback
            logger.info(fb)

            if fb == FeedbackTypes.ZOOM_IN:
                logger.info('please zoom in')
            elif fb == FeedbackTypes.ZOOM_OUT:
                logger.info('please zoom out')
            elif fb == FeedbackTypes.STABLE:
                logger.info('camera is stable')
            elif fb == FeedbackTypes.SORRY:
                logger.info('sorry. can not provide feedback')
            else:
                logger.info('unknown feedback type. sorry')



        except KeyboardInterrupt:
            logger.error('Exiting due to keyboard interrupt')
            cv2.destroyAllWindows()
            break






