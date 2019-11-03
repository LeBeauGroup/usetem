import pluginTypes as pluginTypes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np



class ForLoop(pluginTypes.IExtensionPlugin):

    def __init__(self):

        super(ForLoop, self).__init__()
        self.defaultParameters.update({'start': '1', 'step': '1', 'stop': '10', 'variableName': 'None'})
        self.acceptsChildren = True



    def run(self, input=None):

        print('trying to run ')
        start = float(input['start'])
        step = float(input['step'])
        stop = float(input['stop'])

        values = np.arange(start, stop, step)

        return values.tolist()
