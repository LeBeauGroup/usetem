import pluginTypes as pluginTypes
from PyQt5 import QtCore, QtGui, QtWidgets


class ForLoop(pluginTypes.IExtensionPlugin):

    def __init__(self):

        super(ForLoop, self).__init__()
        self.defaultParameters.update({'start': '1', 'step': '1', 'stop': '10', 'variableName': 'None'})
        self.acceptsChildren = True

    def run(self, input=None):

        # itemToRun : QtWidgets.QTreeWidgetItem = input
        #
        # if itemToRun.childCount() > 0:
        #     print('more children to run')
        #
        #     for ind in range(itemToRun.childCount()):
        #
        #         childToRun = itemToRun.child(ind)
        #         self.run(childToRun)
        # else:


        print('running loop')

        return