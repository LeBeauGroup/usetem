import logging
from comtypes.gen import ESVision

logging.basicConfig(level=logging.INFO)

class ProcessingSystem():

    def __init__(self, app):
        self.prosys = app.ProcessingSystem()
        self.app = app

    def variance(self, objectPath):

        theObject = self.app.FindDisplayObject(objectPath).QueryInterface(ESVision.IImage)
        var = self.prosys.Variance(theObject.Data).Real

        return var


