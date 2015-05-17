import glob
import os
import multiprocessing as mp
import numpy as np
from scipy.spatial import KDTree
from PIL import Image
import timeit

BASEPATH = os.path.join(os.path.dirname(__file__))
IMGDIR = os.path.join(BASEPATH, "images")

def listAllFiles():
    return [e.replace("\\", "/") for e in glob.glob(os.path.join(IMGDIR, "*.jpg"))]

def getAverageColor(pic):
    img = Image.open(pic)
    width, height = img.size
    numPixels = width * height
    pixels = img.load()
    rgb = np.array([0,0,0])
    for x in xrange(width):
        for y in xrange(height):
            pixel = np.array(pixels[x, y])
            if pixel.size > 3: # discard alpha value
                pixel = pixel[:3]
            rgb = np.add(rgb, pixel)
    rgb = np.divide(rgb, numPixels)
    return rgb

def getAverageColorParallel(pic):
    img = Image.open(pic)
    width, height = img.size
    numPixels = width * height
    pixels = img.load()
    rgb = np.array([0,0,0])
    for x in xrange(width):
        for y in xrange(height):
            pixel = np.array(pixels[x, y])
            if pixel.size > 3: # discard alpha value
                pixel = pixel[:3]
            rgb = np.add(rgb, pixel)
    rgb = np.divide(rgb, numPixels)
    return (tuple(rgb), pic)

def createKDTree(imagefiles):
    imgdict = {}
    for imagefile in imagefiles:
        avgColor = getAverageColor(imagefile)
        imgdict[tuple(avgColor)] = imagefile
    tree = KDTree(imgdict.keys())
    return (tree, imgdict)

def createKDTreeParallel(imagefiles):
    pool = mp.Pool(processes=mp.cpu_count()+2)
    avgColors = pool.map(getAverageColorParallel, imagefiles)
    imgdict = dict(avgColors)
    tree = KDTree(imgdict.keys())
    return (tree, imgdict)

if __name__ == "__main__":
    files = listAllFiles()
    #tree1, dict1 = createKDTree(files)
    #tree2, dict2 = createKDTreeParallel(files)
    print "Regular:", timeit.timeit(lambda: createKDTree(files), number=1)
    print "Parallel:", timeit.timeit(lambda: createKDTreeParallel(files), number=1)
