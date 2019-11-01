import pluginTypes as pluginTypes
from PyQt5 import QtCore, QtGui, QtWidgets


class forLoop(pluginTypes.IExtensionPlugin):

    def __init__(self):

        super(forLoop, self).__init__()
        self.defaultParameters.update({'start':'1', 'step':'1', 'stop':'10'})
        self.acceptsChildren = True

    def run(self, input):
        pass
