from PIL import Image


im = Image.open('test.png')


def get_pixels_table(im):
    s = im.size
    pix = [[() for i in range(s[0])] for j in range(s[1])]
    for i in range(s[1]):
        for j in range(s[0]):
            pix[i][j] = im.getpixel((j,i))

    return pix

def convertToBitset(rgb,mask):
    h = len(rgb)
    w = len(rgb[0])
    res = [0]*h
    for i in range(h):
        res[i] = [0]*w
        for j in range(w):
            res[i][j] = []
    for i in range(h):
        for j in range(w):
            for k in range(len(rgb[i][j])):
                for l in range(8):
                    if mask[k*8+l]==1:
                        if rgb[i][j][k]&(1<<l) > 0:
                            res[i][j].append(1)
                        else:
                            res[i][j].append(0)
    return res

def findInMotif(mat_motif,order_target):
    map = {}
    for i in range(len(mat_motif)):
        for j in range(len(mat_motif[i])):
            map[mat_motif[i][j]] = (i,j)
    return [map[order_target[i]] for i in range(len(order_target))]

def aggregate(data,mat_motif,order_target):
    points = findInMotif(mat_motif,order_target)
    res = []
    n = len(data[0][0])
    h = len(mat_motif)
    w = len(mat_motif[0])//n
    for i in range(0,len(data),h):
        for j in range(0,len(data[i]),w):
            for k in range(len(points)):
                res.append(data[i+points[k][0]][j+points[k][1]//n][points[k][1]%n])
    return res

def reconstruct(pix_base,mask,flipping_bits):
    h = len(pix_base)
    w = len(pix_base[0])
    res = [0]*h
    for i in range(h):
        res[i] = [0]*w
        for j in range(w):
            res[i][j] = pix_base[i][j]
    cur = 0
    for i in range(h):
        for j in range(w):
            for k in range(3):
                for l in range(8):
                    if mask[k*8+l]==1:
                        if flipping_bits[cur] == 1:
                            res[i][j][k] += (1<<l)
                        cur += 1
    return res


mask = [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0]
pix = get_pixels_table(im)
print(pix)
medium = convertToBitset(pix,mask)
print(medium)

reconstruct(pix,mask,[0,1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,1])
