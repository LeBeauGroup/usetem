import usetem.pluginTypes as pluginTypes
from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os
import numpy as np
from PyQt5 import uic



class Conditional(pluginTypes.IExtensionPlugin):

    def __init__(self):

        super(Conditional, self).__init__()
        self.defaultParameters.update({'conditions':list()})
        self.acceptsChildren = False


    def ui(self, item, parent=None):

        filePath = os.path.dirname(os.path.realpath(__file__)) #sys.modules[self.__module__].__file__.split(os.extsep)[0]

        def updateConditional():

            sender = theUI.sender()

            for childIndex in range(0, conditionalItem.childCount()):
                tree = conditionalItem.treeWidget()
                testChild = conditionalItem.child(childIndex)
                testChildWidget = tree.itemWidget(testChild,0)

                if testChildWidget is sender.parent():
                    condition = sender.text()
                    conditionalItem.data['conditions'][childIndex] = condition

        def elseIfUi(elseIfItem, type):
            elseIfFile = QtCore.QFile(filePath + '\elseIf.ui')
            elseIfFile.open(QtCore.QFile.ReadOnly)

            elseIfUi = uic.loadUi(elseIfFile)

            childIndex = conditionalItem.indexOfChild(elseIfItem)

            if type == 'elseIf' and childIndex == 0:
                elseIfUi.label.setText('If')

            elif type == 'elseIf':
                elseIfUi.label.setText('Else If')

            else:
                elseIfUi.label.setText('Else')
                elseIfUi.elseIfEdit.hide()

            elseIfUi.elseIfEdit.editingFinished.connect(updateConditional)

            try:
                elseIfUi.elseIfEdit.setText(conditionalItem.data['conditions'][childIndex])
            except Exception as e:
                print('error' + str(e))

            return elseIfUi

        def addElseIf():

            tree = conditionalItem.treeWidget()
            containsElse = False

            addName = theUI.sender().objectName()

            # Check if there is an else statement, and make sure there isn't already
            if conditionalItem.childCount() > 0:
                lastChild = conditionalItem.child(conditionalItem.childCount()-1)
                if lastChild.data['name'] == 'else':
                    containsElse = True

                    if containsElse and addName == 'addElse':
                        return

            newElseIf = QtWidgets.QTreeWidgetItem(0)
            QtWidgets.QTreeWidgetItem()

            condName = 'elseIf'

            if addName == 'addElse':
                condName = 'else'


            newElseIf.data = {'name': condName}

            print(conditionalItem.data)


            # Find the right index to insert at depending on if there is already an else statement
            insertIndex = conditionalItem.childCount()

            if containsElse:
                insertIndex -= 1
                conditionalItem.data['conditions'].insert(insertIndex, '')
            elif not containsElse and condName == 'else':
                conditionalItem.data['conditions'].append('True')
            else:
                conditionalItem.data['conditions'].append('')

            conditionalItem.insertChild(insertIndex, newElseIf)

            ui = elseIfUi(newElseIf, condName)

            union = QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDropEnabled
            newElseIf.setFlags(union)
            newElseIf.setSizeHint(0,ui.size())

            tree.setItemWidget(newElseIf, 0, ui)

            tree.resetItem(conditionalItem)
            conditionalItem.setExpanded(True)

        print(item.data)

        if item.data['name'] == 'elseIf':
            conditionalItem = item.parent()
            theUI = elseIfUi(item, 'elseIf')

        elif item.data['name'] == 'else':
            conditionalItem = item.parent()
            theUI = elseIfUi(item, 'else')

        else:
            theUI = super(Conditional, self).ui(item, parent)
            widget = theUI.findChild(QtWidgets.QWidget,'widget')
            conditionalItem = item
            widget.addElseIf.clicked.connect(addElseIf)
            widget.addElse.clicked.connect(addElseIf)

        return theUI


    def run(self, params=None, result=None):

        # (?! and | or | not | is | in)(? < !['"])(\b([\w-\.]+)\b)(?!['"]) #variable names
        # (\band | or\b)  # find multiple statements
        # (= > ?)( = < ?)(<= ?) | (>= ?) | (!? == ? |)  # Needs to be fixed
        # (? <= '|")(\w+)(?=' | ") # find string
        # = < | <= | >= |= < | > | < | !? == ?  # comparisons

        return result
