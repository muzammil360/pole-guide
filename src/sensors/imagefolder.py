# from glob import glob as DirFileLister
from os import listdir as DirFileLister
from os.path import join as PathJoiner
from os.path import abspath as getAbsPath
import time


import cv2
import numpy as np

from src.logger import get_logger

class ImageFolder:
    def __init__(self,input_dir, new_size=(-1,-1)):
        self.input_dir = input_dir
        self.new_size = new_size

        # get list of all images
        filelist = DirFileLister(self.input_dir)
        self.filelist = [getAbsPath(PathJoiner(self.input_dir,file)) for file in filelist]

        self.logger = get_logger('ImageFolder')
        self.logger.debug('image folder: {}'.format(self.input_dir))
        self.logger.debug('image list: {}'.format(filelist))

        self.n = len(self.filelist)         # total files in directory
        self.i = 0                          # ith file to be read

        self.t0 = time.time()
        self.dt = 0             # elasped time


    def getReading(self):
        return self.readImage()

    def readImage(self):
            
        
        i = self.i % self.n                  # compute iter 
        fileaddr = self.filelist[i]              # get current file address
        image = cv2.imread(fileaddr)            # read the image

        # resize if new size is given
        if self.new_size[0]>0 and self.new_size[1]>0:
            image = cv2.resize(image,self.new_size)

        self.i+=1                               # increment the pointer 

        return image

    def getReadFreq(self):
        return self.getCurrFPS()

    def getCurrFPS(self):
        epsilon = np.finfo(np.float32).eps

        n_frames = 1.0        # currently computation is based on single frame
        time_diff = self.dt

        fps = float(n_frames)/float(time_diff + epsilon)   # TIP: ensure that both num and den are float
        return fps
