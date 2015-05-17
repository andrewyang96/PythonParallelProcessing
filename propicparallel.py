from PIL import Image
from functools import partial
import numpy as np
import multiprocessing as mp
import timeit

def getAverageColorOfRegion(img, bounds):
    xbounds, ybounds = bounds
    if len(xbounds) != 2 or len(ybounds) != 2:
        raise ValueError("xbounds {0} or ybounds {1} incorrectly configured".format(xbounds, ybounds))
    if xbounds[0] < 0 or ybounds[0] < 0 or xbounds[1] > img.size[0] or ybounds[1] > img.size[1]:
        raise ValueError("xbounds {0} or ybounds {1} out of bounds for image size {2}".format(xbounds, ybounds, img.size))
    numPixels = (xbounds[1] - xbounds[0]) * (ybounds[1] - ybounds[0])
    pixels = img.load()
    rgb = np.array([0,0,0])
    for x in xrange(*xbounds):
        for y in xrange(*ybounds):
            pixel = np.array(pixels[x, y])
            if pixel.size > 3: # discard alpha value
                pixel = pixel[:3]
            rgb = np.add(rgb, pixel)
    rgb = np.divide(rgb, numPixels)
    return rgb

def parseProfilePicture(propic, width=20, height=20):
    if width != height: # ensure square output image
        raise ValueError("Width ({0}) and height ({1}) must be the same".format(width, height))
    if width < 20 or height < 20: # ensure enough images
        raise ValueError("Width and height both must be >= 10")
    img = Image.open(propic)
    imgWidth, imgHeight = img.size
    widthInt, heightInt = float(imgWidth) / width, float(imgHeight) / height
    arr = np.ndarray((height, width, 3))

    for x in xrange(width):
        for y in xrange(height):
            xbounds = (int(x * widthInt), int((x+1) * widthInt))
            ybounds = (int(y * heightInt), int((y+1) * heightInt))
            arr[y][x] = getAverageColorOfRegion(img, (xbounds, ybounds))
    return arr

def parseParallel(propic, width=20, height=20):
    if width != height: # ensure square output image
        raise ValueError("Width ({0}) and height ({1}) must be the same".format(width, height))
    if width < 20 or height < 20: # ensure enough images
        raise ValueError("Width and height both must be >= 10")
    img = Image.open(propic)
    imgWidth, imgHeight = img.size
    widthInt, heightInt = float(imgWidth) / width, float(imgHeight) / height

    pool = mp.Pool(processes=mp.cpu_count()+2)
    bounds = [((int(x * widthInt), int((x+1) * widthInt)), (int(y * heightInt), int((y+1) * heightInt))) for y in xrange(height) for x in xrange(width)]
    func = partial(getAverageColorOfRegion, img)
    arr = pool.map(func, bounds)
    arr = np.reshape(arr, (height, width, 3))
    return arr

def reg():
    return parseProfilePicture("propic.jpg", 50, 50)

def parallel():
    return parseParallel("propic.jpg", 50, 50)

if __name__ == "__main__":
    print "Regular:", timeit.timeit(reg, number=1)
    print "Parallel:", timeit.timeit(parallel, number=1)
