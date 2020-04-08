import time

import cv2
import numpy as np

from src.logger import get_logger


class Camera:
    def __init__(self, device_num):
        self.logger = get_logger('Camera')
        self.logger.debug('constructor start')

        self.cap = cv2.VideoCapture(device_num)
        
        # assert self.cap.isOpened(), 'Cannot capture source'
        if self.cap.isOpened() is False:
            self.logger.critical('Unable to open camera: device{}'.format(device_num))


        self.t0 = time.time()
        self.dt = 0             # elasped time

        self.logger.debug('constructor ends')


    def __del__(self):
        # if camera is open, release it
        if self.cap.isOpened():
            self.cap.release()

    def getReading(self):
        return self.getFrame()

    def getFrame(self):

        # if camera is open, read the frame; otherwise, raise "sensor not open" exception 
        if self.cap.isOpened():
            ret, frame = self.cap.read()

            # note the current time for fps calculation later
            time_now = time.time() 
            self.dt = time_now - self.t0
            self.t0 = time_now         # update the t0 for next iteration

        else:
            # TODO: raise "sensor not open" exception 
            pass

            

        # if frame is valid, return it; otherwise, raise "invalid frame" exception
        if ret:
            return frame
        else:
            # TODO: raise "invalid frame" exception 
            pass

    def getReadFreq(self):
        return self.getCurrFPS()

    def getCurrFPS(self):
        epsilon = np.finfo(np.float32).eps

        n_frames = 1.0        # currently computation is based on single frame
        time_diff = self.dt

        fps = float(n_frames)/float(time_diff + epsilon)   # TIP: ensure that both num and den are float
        return fps
