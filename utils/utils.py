#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
import binascii


# decompose une image [h][w][3] (0->255) selon une composante (0 pour rouge, 1 pour vert, 2 pour bleu)
# retourne [h*w] (0->255)
def decompose_comp(image,comp):
    return image[:,:,comp].ravel()

# decompose une image [h][w][3] selon toutes ses composantes et retourne la concatenation des 3 composantes
# retourne [h*w*3] (0->255)
def decompose(image):
    image_R = image[:,:,0].ravel()
    image_G = image[:,:,1].ravel()
    image_B = image[:,:,2].ravel()
    return np.hstack((image_R,image_G,image_B))

# decompose une image [h][w][3] en ses bits de poids faibles
# retourne [h*w*3] (0->1)
def decompose_lsb(image):
    tmp = decompose(image)
    for i in range(len(tmp)):
        tmp[i] = tmp[i]&1
    return tmp

# recompose une image a partir de la taille d'une image initiale et d'un tableau de pixel [h*w*3] (0->255)
# retourne une Image
def imageRecompose(imageVectorized,imageInitiale):
    shape = imageInitiale[:,:,0].shape
    length = len(imageVectorized)/3
    image_R = imageVectorized[0:length].reshape(shape)
    image_G = imageVectorized[length:2*length].reshape(shape)
    image_B = imageVectorized[2*length:].reshape(shape)

    image = imageInitiale.copy()
    image[:,:,0] = image_R
    image[:,:,1] = image_G
    image[:,:,2] = image_B

    return image


# convertit une chaine de caracteres en chaine binaire
def textToBin(text):
    string = ''
    for char in text:
        binString = bin(int(binascii.hexlify(char), 16))[2:]
        while len(binString)<8:
            binString = '0'+binString
        string += binString

    return string

# convertit une chaine binaire en chaine de caracteres
def binToText(binaryString):
    ret = ''
    for i in range(0,len(binaryString),8) :
        octet = binaryString[i:i+8]
        n = int(octet,2)
        ret += binascii.unhexlify('%x' % n)

    return ret

# met a zero les l premieres valeur du tableau
# retourne le tableau modifie
def clearLSB(array,l):
    for index,color in enumerate(array):
        if color%2==1 and index<=l:
            array[index]-=1
    return array
