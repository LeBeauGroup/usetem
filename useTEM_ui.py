# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject
from extensions.revSTEM import revSTEM


class UseTEMUI(object):


    def setupUi(self, MainWindow, plugins):
        self.plugins = plugins
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(809, 609)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.availablePlugins = QtWidgets.QTreeWidget(self.centralwidget)
        self.availablePlugins.setGeometry(QtCore.QRect(0, 0, 221, 561))
        self.availablePlugins.setObjectName("availablePlugins")
        self.availablePlugins.headerItem().setText(0, "1")
        self.workflow = QtWidgets.QTreeWidget(self.centralwidget)
        self.workflow.setGeometry(QtCore.QRect(220, 0, 591, 561))
        self.workflow.setObjectName("workflow")
        self.workflow.headerItem().setText(0, "1")
        self.statusLabel = QtWidgets.QLabel(self.centralwidget)
        self.statusLabel.setGeometry(QtCore.QRect(440, 570, 46, 13))
        self.statusLabel.setObjectName("statusLabel")
        self.addButton = QtWidgets.QPushButton(self.centralwidget)
        self.addButton.setGeometry(QtCore.QRect(200, 560, 21, 23))
        self.addButton.setObjectName("addButton")
        self.removeButton = QtWidgets.QPushButton(self.centralwidget)
        self.removeButton.setGeometry(QtCore.QRect(220, 560, 21, 23))
        self.removeButton.setObjectName("removeButton")
        self.runButton = QtWidgets.QPushButton(self.centralwidget)
        self.runButton.setGeometry(QtCore.QRect(600, 560, 75, 23))
        self.runButton.setObjectName("runButton")
        self.cancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancelButton.setGeometry(QtCore.QRect(730, 560, 75, 23))
        self.cancelButton.setObjectName("cancelButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 809, 18))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        #self.workflow = QtWidgets.QTreeWidget(MainWindow)
        self.workflow.setColumnCount(1)
        # self.listWidget.setGeometry(QtCore.QRect(10, 10, 371, 211))
        # self.listWidget.setObjectName("listWidget")

        #self.listWidget.setExpanded(0,True);

        # setup plugin views
        #for plugin in plugins:


        self.runButton.clicked.connect(self.runWorkflow)
        self.addButton.clicked.connect(self.addToWorkflow)

        self.removeButton.clicked.connect(self.removeFromWorkflow)




       #  print('setup widget')
       #  item = QtWidgets.QTreeWidgetItem(self.listWidget)
       #  item_widget2 = test_plugin_ui2.Ui_Form('blash')
       # # item.setSizeHint(QtCore.QSize(100,50))
       #  self.listWidget.addTopLevelItem(item)
       #  self.listWidget.setItemWidget(item,0,item_widget2)

    def addToWorkflow(self):

        selected = self.availablePlugins.selectedItems()

        item = QtWidgets.QTreeWidgetItem(self.workflow)

        item_widget = revSTEM('blash',self.plugins)
        self.workflow.addTopLevelItem(item)
        self.workflow.setItemWidget(item,0,item_widget)



    def removeFromWorkflow(self):

        # returns a QList
        selected = self.workflow.selectedItems()


        # TODO: Deal with children removal
        for obj in selected:

            index = self.workflow.indexOfTopLevelItem(obj)
            self.workflow.takeTopLevelItem(index)

    def runWorkflow(self):

        for itemIndex in range(4203493523):

            topLevelItem = self.workflow.topLevelItem(itemIndex)

            if topLevelItem.childCount() > 0:
                print('Children to run!')
            else:
                print('trying to run')
                self.workflow.itemWidget(topLevelItem,0).run()



    def reject(self):
        print('rejected!')

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.statusLabel.setText(_translate("MainWindow", "Status"))
        self.addButton.setText(_translate("MainWindow", "+"))
        self.removeButton.setText(_translate("MainWindow", "-"))
        self.runButton.setText(_translate("MainWindow", "Run"))
        self.cancelButton.setText(_translate("MainWindow", "Cancel"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))

