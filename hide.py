#!/usr/bin/python

import os
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
os.sys.path.insert(0,parentdir)

from utils import utils
from PIL import Image
import numpy as np


# find the most appropriate parameter for Hamming :  this is the biggest k that allows blocks of k bits of message to fit in medium in blocks of 2**k-1 bits
def find_best_k(size_message,size_medium):
    k = 2
    good = False
    while not good:
        k += 1
        n_message_blocs = size_message//k
        n = 2**k-1
        n_medium_blocs = size_medium//n
        if n_message_blocs>=n_medium_blocs:
            good = True
            if size_message%k != 0 or n_message_blocs>n_medium_blocs:
                k -= 1
    if k>12:
        return 12
    return k

# convert string to binary array
def to_binary_array(text):
    binary = utils.textToBin(text)
    return [ord(i)-ord('0') for i in binary]

# apply the algorithm of Hamming syndrom in order to toggle some bits in medium
def hidden_array(bin_message,bin_image,H,k):
    n = 0
    ret = []
    for i in range(0,len(bin_message),k):
        m = bin_message[i:i+k]
        x = bin_image[n:n+2**k-1]
        n += 2**k-1

        for j in range(len(m),k):
            m.append(0)
        for j in range(len(x),2**k-1):
            x = np.append(x,0)

        v = utils.binarize_array(m-(H.dot(x)))

        index = -1
        for j in range(H.shape[1]):
            if np.array_equal(H[:,j],v):
                index = j
                break

        if index >= 0:
            x[index] = 1-x[index]
        ret.extend(x)

    return ret

# hide a message in image
def hide(image,message):
    binary = to_binary_array(message+'\x00')
    image_vectorized_lsb = utils.decompose_lsb(image)
    k = find_best_k(len(binary),len(image_vectorized_lsb))
    G,H = utils.create_hamming(k)

    print("Best k found : "+str(k))

    hidden_data = hidden_array(binary,image_vectorized_lsb,H,k)

    hamming_lsb_vectorized = utils.clearLSB(utils.decompose(image),len(hidden_data))
    for i in range(len(hidden_data)):
        hamming_lsb_vectorized[i] += hidden_data[i]

    return utils.imageRecompose(hamming_lsb_vectorized,image)


import argparse

parser = argparse.ArgumentParser(description='Hide a message in image')
parser.add_argument('message', metavar='message',
                    help='a message to hide')
parser.add_argument('image', metavar='input',
                    help='medium in which message should be hidden')
parser.add_argument('output', metavar='output',
                    help='path in which steganoed image should be put')

args = parser.parse_args()

image = np.array(Image.open(args.image))
image_steg = hide(image,args.message)
out = Image.fromarray(image_steg)
out.save(args.output)
