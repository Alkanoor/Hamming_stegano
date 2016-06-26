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

parser = argparse.ArgumentParser(description='Compare histograms of images')
parser.add_argument('image', metavar='image', nargs='+',
                    help='images we want compute histogram of')
parser.add_argument('--min_color', metavar='min_color',
                    help='starting point of histograms')
parser.add_argument('--max_color', metavar='max_color',
                    help='ending point of histograms')
parser.add_argument('--component', metavar='component',
                    help='component to capture (default : red)')

args = parser.parse_args()

images = args.image

m = 50
M = 70
if args.min_color is not None and args.max_color is not None:
    m = args.min_color
    M = args.max_color

component = 'red'
if  args.component is not None:
    component = args.component


for i in range(len(images)):
    image = np.array(Image.open(images[i]))
    if component == 'red':
        image_decomposed = utils.decompose_comp(image,0)
    elif compoennt == 'green':
        image_decomposed = utils.decompose_comp(image,1)
    else:
        image_decomposed = utils.decompose_comp(image,2)
    index = []
    for j in range(len(image_decomposed)):
        if image_decomposed[j] >= m and image_decomposed[j] <= M:
            index.append(j)
    image_decomposed_zoomed = image_decomposed[index]
    plt.figure()
    plt.hist(image_decomposed_zoomed,M-m)

    tmp = images[i].split('/')
    tmp = tmp[-1]
    tmp = tmp.split('\\')
    tmp = tmp[-1]
    plt.savefig("histogram_"+component+"_"+tmp)

plt.show()
