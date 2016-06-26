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

parser = argparse.ArgumentParser(description='Compare chi square of images')
parser.add_argument('image', metavar='image', nargs='+',
                    help='images we want compute chi square of')

args = parser.parse_args()

images = args.image


n_points = 1000
def getFrequencies(image,n_points=n_points):
    imageVect = utils.decompose(image)
    length = len(imageVect)
    y=[]
    for i in range(n_points-1):
        y.append(np.mean(imageVect[(i*length)/n_points:((i+1)*length)/n_points]%2))

    y.append(np.mean(imageVect[(n_points-1)*length/n_points:]%2))
    return y


for i in range(len(images)):
    y = getFrequencies(np.array(Image.open(images[i])))

    tmp = images[i].split('/')
    tmp = tmp[-1]
    tmp = tmp.split('\\')
    tmp = tmp[-1]

    plt.figure()
    plt.axis([0,n_points,0,1])
    plt.scatter(range(n_points),y)
    plt.plot(range(n_points),0.5*np.ones(n_points),color = 'black')
    plt.plot(range(n_points),0.45*np.ones(n_points),color='blue')
    plt.plot(range(n_points),0.55*np.ones(n_points),color = 'blue')
    plt.title(tmp)

    plt.savefig("Chi_square_"+tmp)

plt.show()
