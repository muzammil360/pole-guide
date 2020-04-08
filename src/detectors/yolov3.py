import sys
import os
import random 

import cv2
import torch
from torch.autograd import Variable
import pickle as pkl

from src.logger import get_logger
from src.otherparty.pytorch_yolo.darknet import Darknet
from src.otherparty.pytorch_yolo.util import *


def prep_image(img, inp_dim):
    """
    Prepare image for inputting to the neural network. 
    
    Returns a Variable 
    """

    orig_im = img
    dim = orig_im.shape[1], orig_im.shape[0]
    img = cv2.resize(orig_im, (inp_dim, inp_dim))
    img_ = img[:,:,::-1].transpose((2,0,1)).copy()
    img_ = torch.from_numpy(img_).float().div(255.0).unsqueeze(0)
    return img_, orig_im, dim


def write(x, img, classes, colors):
    c1 = tuple(x[1:3].int())
    c2 = tuple(x[3:5].int())
    cls = int(x[-1])
    label = "{0}".format(classes[cls])
    color = random.choice(colors)
    cv2.rectangle(img, c1, c2,color, 1)
    t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 1 , 1)[0]
    c2 = c1[0] + t_size[0] + 3, c1[1] + t_size[1] + 4
    cv2.rectangle(img, c1, c2,color, -1)
    cv2.putText(img, label, (c1[0], c1[1] + t_size[1] + 4), cv2.FONT_HERSHEY_PLAIN, 1, [225,255,255], 1);
    return img

class Yolov3:
    def __init__(self,config_addr, 
        weights_addr, 
        input_dim, 
        confidence, 
        num_classes, 
        nms_theshold,
        class_name_fileaddr,
        color_pallete_fileaddr,
        visualize_output):

        self.logger = get_logger('Yolov3')
        self.logger.debug('constructor start')

        self.model = Darknet(config_addr)
        self.model.load_weights(weights_addr)

        self.model.net_info["height"] = input_dim
        self.input_dim = int(self.model.net_info["height"])

        # make sure input dim is > 32 and a multiple of 32
        if (self.input_dim % 32 == 0) is False:
            self.logger.critical('assertion failed: self.input_dim % 32 == 0')
        if (self.input_dim > 32) is False:
            self.logger.critical('assertion failed: self.input_dim > 32')

        # copy the model to GPU is cuda is available
        if torch.cuda.is_available():
            self.model.cuda()
            self.logger.info('using GPU')
        else:
            self.logger.info('using CPU')

            
        # put the model to inference mode
        self.logger.info('putting model to eval mode')
        self.model.eval()



        # set parameters for later use
        self.confidence = confidence
        self.num_classes = num_classes
        self.nms_theshold = nms_theshold
        self.visualize_output = visualize_output

        # load class names
        self.classes = load_classes(class_name_fileaddr)
        self.colors = pkl.load(open(color_pallete_fileaddr, "rb"))


    def detect(self, image):
        # pre-process the images
        img_prepped, _ , orig_img_dim = prep_image(image, self.input_dim)

        # copy the image to GPU if available
        if torch.cuda.is_available():
            img_prepped = img_prepped.cuda()


        # forward propagate the images
        detections = self.model(Variable(img_prepped), torch.cuda.is_available())


        # post-processing
        inp_dim = self.input_dim
        output = write_results(detections, self.confidence, self.num_classes, nms = True, nms_conf = self.nms_theshold)

        if len(output)>0:
            output[:,1:5] = torch.clamp(output[:,1:5], 0.0, float(inp_dim))/inp_dim 
            output[:,[1,3]] *= image.shape[1]
            output[:,[2,4]] *= image.shape[0]

            output = filterPredictions(output,keep_cls=[0])


        if self.visualize_output:
            list(map(lambda x: write(x, image, self.classes, self.colors), output))      
            cv2.imshow("image", image)
            key = cv2.waitKey(1)
        
        return output
         