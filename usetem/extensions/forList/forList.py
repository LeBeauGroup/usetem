import useTEM.pluginTypes as pluginTypes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np



class ForList(pluginTypes.IExtensionPlugin):

    def __init__(self):

        super(ForList, self).__init__()
        self.defaultParameters.update({'listItems': [], 'variableName': 'None'})
        self.acceptsChildren = True

    def ui(self, item, parent=None):
        superUi = super(ForList, self).ui(item)

        def updateListData(listWidget):

            loopList = list()
            for ind in range(listWidget.count()):

                loopList.append(listWidget.item(ind).text())

            widget.item.data['listItems'] = loopList

        def moveUp():
            listWidget:QtWidgets.QListWidget = widget.findChildren(QtWidgets.QListWidget, 'listItemsView')[0]

            currentRow = listWidget.currentRow()
            holder = listWidget.takeItem(currentRow)
            listWidget.insertItem(currentRow-1, holder)
            updateListData(listWidget)

        def moveDown():
            listWidget: QtWidgets.QListWidget = widget.findChildren(QtWidgets.QListWidget, 'listItemsView')[0]

            currentRow = listWidget.currentRow()
            holder = listWidget.takeItem(currentRow)
            listWidget.insertItem(currentRow+1, holder)

            updateListData(listWidget)

        def remove():
            listWidget: QtWidgets.QListWidget = widget.findChildren(QtWidgets.QListWidget, 'listItemsView')[0]

            currentRow = listWidget.currentRow()
            holder = listWidget.takeItem(currentRow)

            updateListData(listWidget)


        widget = superUi.findChild(QtWidgets.QWidget, 'widget')

        moveUpButton = widget.findChildren(QtWidgets.QPushButton, 'moveListItemUpButton')[0]
        moveDownButton = widget.findChildren(QtWidgets.QPushButton, 'moveListItemDownButton')[0]
        moveUpButton.clicked.connect(moveUp)
        moveDownButton.clicked.connect(moveDown)

        removeButton = widget.findChildren(QtWidgets.QPushButton, 'removeListItemUpButton')[0]
        removeButton.clicked.connect(remove)

        return superUi

    def run(self, params=None, result=None):


        return params['listItems']
