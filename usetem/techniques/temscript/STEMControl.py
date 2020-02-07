import usetem.pluginTypes as pluginTypes
import abc
import numpy as np
import pickle

class ISTEMControl(pluginTypes.ITechniquePlugin):

    client = None
    instrument = None

    def scanRotation(self, angle=None):
        """
        angle in degrees
        """

        if angle is None:
			return client.illumination.stemRotation()
        else:
            client.illumination.stemRotation(angle)



