import pluginTypes as pluginTypes
from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os
import numpy as np
from PyQt5 import uic



class Conditional(pluginTypes.IExtensionPlugin):

    def __init__(self):

        super(Conditional, self).__init__()
        self.defaultParameters.update({'conditions':{}})
        self.acceptsChildren = False


    def ui(self, item, parent=None):

        filePath = os.path.dirname(os.path.realpath(__file__)) #sys.modules[self.__module__].__file__.split(os.extsep)[0]

        def updateConditional():
            sender = theUI.sender()

            conditionName = sender.parent().objectName()
            condition = sender.text()
            conditionalItem.data['conditions'].update({conditionName:condition})

            print(conditionalItem.data)

        def elseIfUi(elseIfItem):
            elseIfFile = QtCore.QFile(filePath + '\elseIf.ui')
            elseIfFile.open(QtCore.QFile.ReadOnly)

            elseIfUi = uic.loadUi(elseIfFile)
            childIndex = conditionalItem.indexOfChild(elseIfItem)

            if childIndex == 0:
                elseIfUi.label.setText('If')
            else:
                elseIfUi.label.setText('Else If')

            elseIfUi.elseIfEdit.editingFinished.connect(updateConditional)
            dictKey = 'ifCondition' + str(childIndex)
            elseIfUi.setObjectName(dictKey)

            try:
                elseIfUi.elseIfEdit.setText(conditionalItem.data['conditions'][dictKey])
            except Exception as e:
                pass

            return elseIfUi

        def addElseIf():

            tree = conditionalItem.treeWidget()

            newElseIf = QtWidgets.QTreeWidgetItem(conditionalItem,0)
            newElseIf.data = {'name': 'elseIf'}

            ui = elseIfUi(newElseIf)

            union = QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDropEnabled
            newElseIf.setFlags(union)

            newElseIf.setSizeHint(0,ui.size())

            tree.setItemWidget(newElseIf, 0, ui)
            conditionalItem.setExpanded(True)

        if item.data['name'] == 'elseIf':
            conditionalItem = item.parent()
            theUI = elseIfUi(item)
        else:
            theUI = super(Conditional, self).ui(item, parent)
            conditionalItem = item
            theUI.addElseIf.clicked.connect(addElseIf)

        return theUI


    def run(self, params=None, result=None):

        # (?! and | or | not | is | in)(? < !['"])(\b([\w-\.]+)\b)(?!['"]) #variable names
        # (\band | or\b)  # find multiple statements
        # (= > ?)( = < ?)(<= ?) | (>= ?) | (!? == ? |)  # Needs to be fixed
        # (? <= '|")(\w+)(?=' | ") # find string
        # = < | <= | >= |= < | > | < | !? == ?  # comparisons

        return result
