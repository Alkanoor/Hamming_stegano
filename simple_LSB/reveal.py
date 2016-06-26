#!/usr/bin/python

import os
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
os.sys.path.insert(0,parentdir)

from utils import utils
from PIL import Image
import numpy as np


# extract message from lsb
def extractMessage(imageDeco):
    n_octet = len(imageDeco)/8
    binaryString=''
    for i in range(n_octet):
        octet =''
        for j in range(8):
            if imageDeco[i*8+j]%2==0:
                octet+='0'
            else:
                octet+='1'
        if octet != '00000000':
            binaryString+=octet
        else:
            break

    return utils.binToText(binaryString)


import argparse

parser = argparse.ArgumentParser(description='Reveal a message in image')
parser.add_argument('image', metavar='input',
                    help='an image in which message has been hidden')

args = parser.parse_args()

image_steg = np.array(Image.open(args.image))
imageVectorized = utils.decompose(image_steg)
print('Message decoded :')
print(extractMessage(imageVectorized))
