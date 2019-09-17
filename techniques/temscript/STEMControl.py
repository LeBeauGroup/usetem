from launch.pluginTypes import ITechniquePlugin
import abc
import numpy as np
import pickle

class ISTEMControl(ITechniquePlugin):

    client = None
    instrument = None

    def cameraLength(self, cl=None):
        """

        :param cl: camera length in mm
        :return: camera length in mm if cl not none
        """
        if cl is None:
            return client.projection.cameraLength()
        else:
            client.projection.cameraLength(angle)


    def scanRotation(self, angle=None):
        """
        angle in degrees
        """

        if angle is None:
			return client.illumination.stemRotation()
        else:
            client.illumination.stemRotation(angle)



