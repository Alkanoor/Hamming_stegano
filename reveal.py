#!/usr/bin/python

import os
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
os.sys.path.insert(0,parentdir)

from utils import utils
from PIL import Image
import numpy as np


# extract message from image, with Hamming parameter k
def recover(image,k):
    image_vectorized_lsb = utils.decompose_lsb(image)
    n = 2**k-1
    G,H = utils.create_hamming(k)

    cur_byte = ''
    ret = ''
    for i in range(0,len(image_vectorized_lsb),n):
        y = image_vectorized_lsb[i:i+n]

        for j in range(len(y),n):
            y = np.append(y,0)

        m = utils.binarize_array(H.dot(y))

        for j in m:
            cur_byte += chr(j+ord('0'))
        while len(cur_byte)>8:
            ret += chr(int(cur_byte[:8],2))
            if ret[len(ret)-1] == '\x00':
                return ret
            cur_byte = cur_byte[8:]

    return ret


import argparse

parser = argparse.ArgumentParser(description='Reveal a message in image')
parser.add_argument('image', metavar='input',
                    help='an image in which message has been hidden')
parser.add_argument('--k', metavar='k',
                    help='optional parameter for hamming code. If not specified all are tested between k=3 and k=12')

args = parser.parse_args()

image_steg = np.array(Image.open(args.image))

if args.k is not None:
    print('Message decoded for k = '+args.k+' :')
    print(recover(image_steg,int(args.k)))
else:
    for i in range(3,13):
        print('Message decoded for k = '+str(i)+' :')
        print(recover(image_steg,i))
