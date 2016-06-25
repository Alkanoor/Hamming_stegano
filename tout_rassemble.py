import numpy as np
import matplotlib.pyplot as plt
import binascii
from PIL import Image



image = np.array(Image.open('cosmos.png'))
#plt.figure(figsize=(15,9))
#plt.imshow(image)
#plt.show()


def decompose_comp(image,comp):
    return image[:,:,comp].ravel()

def decompose(image):
    image_R = image[:,:,0].ravel()
    image_G = image[:,:,1].ravel()
    image_B = image[:,:,2].ravel()
    
    return np.hstack((image_R,image_G,image_B))

def decompose_lsb(image):
    tmp = decompose(image)
    for i in range(len(tmp)):
        tmp[i] = tmp[i]&1
    return tmp

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


def textToBin(text):
    string = ''
    for char in text:
        binString = bin(int(binascii.hexlify(char), 16))[2:]
        while len(binString)<8:
            binString = '0'+binString
        string += binString
        
    return string

def binToText(binaryString):
    ret = ''
    
    for i in range(0,len(binaryString),8) :
        octet = binaryString[i:i+8]
        n = int(octet,2)
        ret += binascii.unhexlify('%x' % n)
    return ret


def clearLSB(array,l):
    for index,color in enumerate(array):
        if color%2==1 and index<=l:
            array[index]-=1
    return array

def hideText(imageDeco,texte):
    if len(imageDeco)/8 < len(texte):
        raise Warning("texte trop long pour l'image")
        return
    
    binary = textToBin(texte)
    binary +='00000000'
    for i in range(len(binary)/8):
        octet = binary[i*8:i*8+8]
        for index,byte in enumerate(octet):
            if int(byte) == 1:
                imageDeco[8*i+index]+=1
    
    return imageDeco

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
        #print 'octet:',octet
        if octet != '00000000':
            binaryString+=octet
        
        else:
            #print 'OCTET DE FIN'
            break
    #print binaryString
    #print len(binaryString)
    return binToText(binaryString)


def stegano(image,text):
    imageVectorized = decompose(image)
    image_clear = clearLSB(imageVectorized,(len(text)+1)*8)
    image_input= hideText(image_clear,text)
    return imageRecompose(image_input,image)


def getMessage(image_steg):
    print 'Message decoding ...'
    imageVectorized = decompose(image_steg)
    print 'message decoded :\n',extractMessage(imageVectorized)


image_steg = stegano(image,'Mon code de carte bleue: 9831')
out = Image.fromarray(image_steg)
#out.save('stegnoed.png')
#
#plt.figure(figsize=(15,5))
#plt.subplot(1,2,1)
#plt.imshow(image_steg)
#plt.title('Image Steganographiee')
#plt.subplot(1,2,2)
#plt.imshow(image)
#plt.title('Image originale')
#plt.show()

getMessage(image_steg)


#m = 10
#M = 40
#
#image_r = decompose_comp(image,0)
#index = []
#for i in range(len(image_r)):
#    if image_r[i] >= m and image_r[i] <= M:
#        index.append(i)
#image_r_zoomed = image_r[index]
#plt.hist(image_r_zoomed,30)
#
#image_steg = stegano(image,'bonjour maman comment ca va tu me manques bisous'*20)
#result = Image.fromarray(image_steg)
#result.save('classical_lsb.png')
#image_r_steg = decompose_comp(image_steg,0)
#index = []
#for i in range(len(image_r_steg)):
#    if image_r_steg[i] >= m and image_r_steg[i] <= M:
#        index.append(i)
#image_r_steg_zoomed = image_r_steg[index]
#plt.figure()
#plt.hist(image_r_steg_zoomed,30)
#plt.show()


def log2(n):
    c = 0
    while n>1:
        n //= 2
        c += 1
    return c

def binarize_array(a):
    for i in range(len(a)):
        a[i] = a[i]%2
    return a

def binarize_matrix(m):
    for i in range(len(m)):
        for j in range(len(m[i])):
            m[(i,j)] = m[(i,j)]%2
    return m

def create_hamming(k):
    n = 2**k-1
    m = n-k

    G = np.diag([1]*m)
    H = np.diag([1]*(n-m))
    P = np.zeros([m,n-m])
    o = 0
    for i in range(1,n+1):
        if 2**(log2(i)) != i:
            for j in range(k):
                P[(o,j)] = ((i&(1<<j))>>j)
            o += 1
    return np.concatenate((G,P.T),axis=0),np.concatenate((P.T,H),axis=1)

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

def to_binary_array(text):
    binary = textToBin(text)
    return [ord(i)-ord('0') for i in binary]


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

        v = binarize_array(m-(H.dot(x)))
        
        index = -1
        for j in range(H.shape[1]):
            if np.array_equal(H[:,j],v):
                index = j
                break
            
        if index >= 0:
            x[index] = 1-x[index]
        ret.extend(x)
    
    return ret

def hide(image,message):
    binary = to_binary_array(message+'\x00')
    image_vectorized_lsb = decompose_lsb(image)
    k = find_best_k(len(binary),len(image_vectorized_lsb))
    G,H = create_hamming(k)
    
    hidden_data = hidden_array(binary,image_vectorized_lsb,H,k)
    
    hamming_lsb_vectorized = clearLSB(decompose(image),len(hidden_data))
    for i in range(len(hidden_data)):
        hamming_lsb_vectorized[i] += hidden_data[i]
    
    return imageRecompose(hamming_lsb_vectorized,image)
    
steg_other = hide(image,'bonjour maman comment ca va tu me manques bisous'*20)
result = Image.fromarray(steg_other)
result.save('out.png')

image_steg = stegano(image,'bonjour maman comment ca va tu me manques bisous'*20)
result = Image.fromarray(image_steg)
result.save('classical_lsb.png')