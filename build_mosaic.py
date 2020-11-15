import os
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import pdb

from add_pieces_mosaic import *
from parameters import *


def load_pieces(params: Parameters):
    # citeste toate cele N piese folosite la mozaic din directorul corespunzator
    # toate cele N imagini au aceeasi dimensiune H x W x C, unde:
    # H = inaltime, W = latime, C = nr canale (C=1  gri, C=3 color)
    # functia intoarce pieseMozaic = matrice N x H x W x C in params
    # pieseMoziac[i, :, :, :] reprezinta piesa numarul i

    # citeste imaginile din director
    filenames = os.listdir(params.small_images_dir)
    images = []
    for image_name in filenames:
        img_current = cv.imread(params.small_images_dir +"\\"+ image_name)
        images.append(img_current)
    
    images = np.array(images)

    if params.show_small_images:
        for i in range(10):
            for j in range(10):
                plt.subplot(10, 10, i * 10 + j + 1)
                # OpenCV reads images in BGR format, matplotlib reads images in RBG format
                im = images[i * 10 + j].copy()
                # BGR to RGB, swap the channels
                im = im[:, :, [2, 1, 0]]
                plt.imshow(im)
        plt.show()
    params.small_images = images


def compute_dimensions(params: Parameters):
    # calculeaza dimensiunile mozaicului
    # obtine si imaginea de referinta redimensionata avand aceleasi dimensiuni ca mozaicul

    # calculeaza automat numarul de piese pe verticala
    
    H,W,C=params.image.shape
    nr_mozaic_pieces,h_mozaic, w_mozaic,c=params.small_images.shape
   
    
    # redimensioneaza imaginea
    #noua latime este egala cu nr.piese orizontala * latimea unei piese de mozaic
    new_w = params.num_pieces_horizontal*w_mozaic
    #pastram raportul H/W de la imaginea intiala
    new_h = int((new_w*H)/W)-int((new_w*H)/W)%h_mozaic
    
    params.num_pieces_vertical = int(new_h/h_mozaic)

    
    params.image_resized = cv.resize(params.image, (new_w, new_h))
    
    

def build_mosaic(params: Parameters):
    # incarcam imaginile din care vom forma mozaicul
    load_pieces(params)
    # calculeaza dimensiunea mozaicului
    compute_dimensions(params)

    img_mosaic = None
    if params.layout == 'caroiaj':
        if params.hexagon is True:
            img_mosaic = add_pieces_hexagon(params)
        else:
            img_mosaic = add_pieces_grid(params)
    elif params.layout == 'aleator':
        img_mosaic = add_pieces_random(params)
    else:
        print('Wrong option!')
        exit(-1)

    return img_mosaic