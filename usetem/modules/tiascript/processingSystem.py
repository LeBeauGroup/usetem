import logging
from comtypes.gen import ESVision
from skimage.morphology import square, disk
from scipy import ndimage
from skimage import filters
import numpy as np
from comtypes.safearray import safearray_as_ndarray

logging.basicConfig(level=logging.INFO)

class ProcessingSystem():

    def __init__(self, app):
        self.prosys = app.ProcessingSystem()
        self.app = app

    def variance(self, objectPath):

        theObject = self.app.FindDisplayObject(objectPath).QueryInterface(ESVision.IImage)
        #var = self.prosys.Variance(theObject.Data).Real

        arr = np.array(theObject.Data.array)

        noiseReduced = ndimage.uniform_filter(arr,5)

        var = ndimage.variance(noiseReduced)
        logging.info(var)


        return float(var)


