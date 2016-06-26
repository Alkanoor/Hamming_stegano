#!/usr/bin/python

import os
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
os.sys.path.insert(0,parentdir)

import matplotlib.pyplot as plt
from utils import utils
from PIL import Image
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Compare lsb of images')
parser.add_argument('image', metavar='image', nargs='+',
                    help='images we want compute differences of lsb. First one is reference')
parser.add_argument('--component', metavar='component',
                    help='component to capture (default : red)')

args = parser.parse_args()

images = args.image

component = 'red'
if  args.component is not None:
    component = args.component


for i in range(len(images)):
    image = np.array(Image.open(images[i]))
    if component == 'red':
        image_decomposed = 255*utils.decompose_lsb_comp(image,0)
    elif compoennt == 'green':
        image_decomposed = 255*utils.decompose_lsb_comp(image,1)
    else:
        image_decomposed = 255*utils.decompose_lsb_comp(image,2)

    tmp = images[i].split('/')
    tmp = tmp[-1]
    tmp = tmp.split('\\')
    tmp = tmp[-1]

    tmp_array = np.append(image_decomposed,np.append(image_decomposed,image_decomposed))
    out = Image.fromarray(utils.imageRecompose(tmp_array,image))
    out.save("LSB_"+component+"_"+tmp)

    if i>0:
        for j in range(len(tmp_array)):
            tmp_array[j] ^= ref[j]
        out = Image.fromarray(utils.imageRecompose(tmp_array,image))
        out.save("LSB_"+component+"_Xor_reference_with_"+tmp)
    else:
        ref = tmp_array.copy()
