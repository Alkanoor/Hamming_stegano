#!/usr/bin/python

import os
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
os.sys.path.insert(0,parentdir)

from utils import utils
from PIL import Image
import numpy as np


# Hide message in lsb
def hideText(imageDeco,texte):
    if len(imageDeco)/8 < len(texte):
        raise Warning("texte trop long pour l'image")
        return

    binary = utils.textToBin(texte)
    binary +='00000000'
    for i in range(len(binary)/8):
        octet = binary[i*8:i*8+8]
        for index,byte in enumerate(octet):
            if int(byte) == 1 and 8*i+index<len(imageDeco):
                imageDeco[8*i+index]+=1

    return imageDeco

# Hide message in image
def stegano(image,text):
    imageVectorized = utils.decompose(image)
    image_clear = utils.clearLSB(imageVectorized,(len(text)+1)*8)
    image_input= hideText(image_clear,text)
    return utils.imageRecompose(image_input,image)



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
image_steg = stegano(image,args.message)
out = Image.fromarray(image_steg)
out.save(args.output)
