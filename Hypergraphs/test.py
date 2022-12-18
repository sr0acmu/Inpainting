import tensorflow as tf

import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import datetime
from math import floor

from models.model import Model
from utils.util import *
from options.test_options import TestOptions

from tqdm import tqdm
from PIL import Image, ImageDraw

def load_image (image_file, config) :
    image = tf.io.read_file (image_file) 
    image = tf.image.decode_jpeg (image, channels=3)
    image = tf.cast (image, dtype=tf.float32)
    image = tf.image.resize (image, [int(config.image_shape[0]/2), int(config.image_shape[1]/2)], method='bicubic')#default=bilinear
    image = image / 255.0

    return image

def load_imag (image_file, config) :
    image = tf.io.read_file (image_file) 
    image = tf.image.decode_jpeg (image, channels=3)
    image = tf.cast (image, dtype=tf.float32)
    image = tf.image.resize (image, [256, 256])
    image = image / 255.0

    return image

def test (config) :
    if config.test_file_path != '' :
        print("*********************************")
        print (config.test_file_path)
        count = 0

        file = open (config.test_file_path)
        for line in file.readlines () :
            if not file.split('.')[-1] in ['jpg', 'png', 'jpeg'] :
                continue
            
            print ('Processing Image -', file)
            if config.random_mask == 1 :
                mask = irregular_mask (config.image_shape[0], config.image_shape[1], config.min_strokes, config.max_strokes)

            if config.random_mask == 2 :
                mask = grid_mask(config.image_shape[0], config.image_shape[1])

            else :
                mask = center_mask (config.image_shape[0], config.image_shape[1])

            gt_image = load_image (os.path.join (root, file), config)
            gt_image = np.expand_dims (gt_image, axis=0)

            #input_image = np.where (mask==1, 1, gt_image)
            input_image = np.zeros(( gt_image.shape[1]*2, gt_image.shape[2]*2, gt_image.shape[3]))
            shp = input_image.shape
            for i in range(0,shp[0]*2):
                for j in range(0,shp[2]*2):
                    if i%2==0 and j%2==0:
                        for k in range(0,shp[3]):
                            input_image[0][i][j][k] = gt_image[0][floor(i/2)][floor(j/2)][k]
                    else:
                        for k in range(0,shp[3]):
                            input_image[0][i][j][k] = 1.
            print (input_image)

            prediction_coarse, prediction_refine = generator ([gt_image, mask], training=False)
            #prediction_refine = prediction_refine * mask + gt_image * (1  - mask)
            #save_images (input_image[0, ...], gt_image[0, ...], prediction_coarse[0, ...], prediction_refine[0, ...], os.path.join (config.testing_dir, file))
            save_images (mask[0, ...], input_image[0, ...], gt_image[0, ...], prediction_refine[0, ...], os.path.join (config.testing_dir, file))
            
            count += 1
            if count == config.test_num :
                return
            print ('-'*20)
    else:
        count = 0
        for root, dirs, files in os.walk (config.test_dir) :
            for file in files :
                if not file.split('.')[-1] in ['jpg', 'png', 'jpeg'] :
                    continue
                
                print ('Processing Image -', file)
                if config.random_mask == 1 :
                    mask = irregular_mask (config.image_shape[0], config.image_shape[1], config.min_strokes, config.max_strokes)
                if config.random_mask == 2 :
                    mask = grid_mask (config.image_shape[0], config.image_shape[1])
                else :
                    mask = center_mask (config.image_shape[0], config.image_shape[1])

                gt_image = load_image (os.path.join (root, file), config)
                gt_image = np.expand_dims (gt_image, axis=0)

                g_image = load_imag (os.path.join (root, file), config)
                g_image = np.expand_dims (gt_image, axis=0)

                print("====", gt_image.shape)

                #input_image = np.where (mask==1, 1, gt_image)
                input_image = np.zeros((gt_image.shape[1]*2, gt_image.shape[2]*2, gt_image.shape[3]))
                for i in range(0,gt_image.shape[1]*2):
                    for j in range(0,gt_image.shape[2]*2):
                        if i%2==0 and j%2==0:
                            for k in range(0,gt_image.shape[3]):
                                input_image[i][j][k] = gt_image[0][floor(i/2)][floor(j/2)][k]
                        else:
                            for k in range(0,gt_image.shape[3]):
                                input_image[i][j][k] = 1.
                #print(input_image)
                #print(gt_image)
                input_image = np.expand_dims(input_image, axis=0)
                g_image = tf.image.resize (gt_image, [256, 256])
                print("input image size = ", input_image.shape)
                print("mask size = ", mask.shape)
                print("gt size = ", g_image.shape)
                #prediction_coarse, prediction_refine = generator ([input_image, mask], training=False)
                prediction_coarse, prediction_refine = generator ([input_image, mask], training=False)
                #prediction_refine = prediction_refine * mask + g_image[0] * (1  - mask)
                save_images (input_image[0, ...], g_image[0, ...], prediction_coarse[0, ...], prediction_refine[0, ...], os.path.join (config.testing_dir, file))
                #save_images (input_image[0, ...], gt_image[0, ...], prediction_coarse[0, ...], prediction_refine[0, ...], os.path.join (config.testing_dir, file))
                #save_images (mask[0, ...], input_image[0, ...], gt_image[0, ...], prediction_refine[0, ...], os.path.join (config.testing_dir, file))
                #print(mask)
                count += 1
                if count == config.test_num :
                    return
                print ('-'*20)

if __name__ == '__main__' :
    # Loading the arguments
    config = TestOptions().parse ()

    model = Model ()
    generator = model.build_generator ()

    checkpoint = tf.train.Checkpoint (generator=generator)
    checkpoint.restore (os.path.join (config.pretrained_model_dir, config.checkpoint_prefix))

    test (config)
