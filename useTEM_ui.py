# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread
import useTEM.pluginManagement as plugm


class MyTreeWidget(QtWidgets.QTreeWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("workflow")
        self.headerItem().setText(0, "1")

        p = self.palette()
        p.setColor(QtGui.QPalette.Highlight, QtGui.QColor('gray'))
        self.setPalette(p)

        # TODO: Use the following to enable drag/drop capabilities
        self.setColumnCount(1)
        self.setAcceptDrops(True)
        # self.setDragEnabled(True)
        # self.setDropIndicatorShown(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)
    # def dropMimeData(self, QTreeWidgetItem, p_int, QMimeData, Qt_DropAction):
    #     print('dropped')
    #
    def dropEvent(self, event):

        mimeData = event.mimeData()

        target = self.itemAt(event.pos())
        dropPos = self.dropIndicatorPosition()

        if dropPos == QtWidgets.QAbstractItemView.BelowItem:
            target = self.itemBelow(target)

        model = self.model()
        model.index()
        model.insertRow(0)


        # dragItem = self.selectedItems()[0]
        # dragWidget = self.itemWidget(dragItem, 0)
        # print(dragWidget)
        #
        # index = self.indexOfTopLevelItem(dragItem)
        #
        # self.takeTopLevelItem(index)
        #
        # self.addTopLevelItem(dragItem)
        # self.setItemWidget(dragItem, 0, dragWidget)

        # model.moveRow(draggedIndex, targetIndex, 0)

        #
        # model.setItemData(draggedIndex, targetData)
        # model.setItemData(targetIndex, draggedData)



        #
        # print(target)
        #
        # widget = self.itemWidget(dragItem ,0)
        # twidget = self.itemWidget(target, 0)
        #
        # print(widget)
        # print(twidget)
        #
        # self.setItemWidget(target, 0, twidget)
        # self.setItemWidget(dragItem, 0, twidget)


        # self.insertTopLevelItem(ind, dragItems[0])

        # QtWidgets.QTreeWidget.dropEvent(event)


    #
    #     event.acceptProposedAction()
    #     # data = event.mimeData().data("application/x-icon-and-text")
    #     print( event.mimeData().text())
    #     event.accept()


class runWorkflowThread(QThread):
    def __init__(self, interfaces, workflow):
        """
        Make a new thread instance with the specified
       workflow from UI.



        :param subreddits: A list of subreddit names
        :type subreddits: list
        """
        QThread.__init__(self)

        self.interfaces = interfaces
        self.workflow = workflow

    def __del__(self):
        self.wait()

    def run(self):

        for itemIndex in range(self.workflow.topLevelItemCount()):

            topLevelItem = self.workflow.topLevelItem(itemIndex)

            if topLevelItem.childCount() > 0:
                print('Children to run!')
            else:
                self.workflow.itemWidget(topLevelItem, 0).extension.setInterfaces(self.interfaces)
                self.workflow.itemWidget(topLevelItem, 0).extension.run()


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

        self.workflow = MyTreeWidget(self.centralwidget)
        self.workflow.setGeometry(QtCore.QRect(220, 0, 591, 561))


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
        # self.listWidget.setGeometry(QtCore.QRect(10, 10, 371, 211))
        # self.listWidget.setObjectName("listWidget")

        #self.listWidget.setExpanded(0,True);

        # setup plugin views

        # TODO: Switch to extensions
        for key in plugins:

            new_item = QtWidgets.QTreeWidgetItem(self.availablePlugins)

            pluginItem = QtWidgets.QLabel()
            pluginItem.setText(key)

            self.availablePlugins.addTopLevelItem(new_item)
            self.availablePlugins.setItemWidget(new_item, 0, pluginItem)


        self.runButton.clicked.connect(self.runWorkflow)
        self.addButton.clicked.connect(self.addToWorkflow)
        self.cancelButton.clicked.connect(self.reject)
        self.removeButton.clicked.connect(self.removeFromWorkflow)

        self.addItem('revSTEM')

       #  print('setup widget')
       #  item = QtWidgets.QTreeWidgetItem(self.listWidget)
       #  item_widget2 = test_plugin_ui2.Ui_Form('blash')
       # # item.setSizeHint(QtCore.QSize(100,50))
       #  self.listWidget.addTopLevelItem(item)
       #  self.listWidget.setItemWidget(item,0,item_widget2)

    def addToWorkflow(self):

        selected = self.availablePlugins.selectedItems()

        for obj in selected:
            label = self.availablePlugins.itemWidget(obj, 0)
            self.addItem(label.text())


        # self.workflow.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
    def addItem(self, name):

        item = QtWidgets.QTreeWidgetItem(self.workflow)

        # use for iterable items | QtCore.Qt.ItemIsDropEnabled
        union = QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled

        item.setFlags(union)
        item.data = name
        item_widget = self.plugins[name].ui()

        self.workflow.addTopLevelItem(item)
        self.workflow.setItemWidget(item, 0, item_widget)

    def removeFromWorkflow(self):

        # returns a QList
        selected = self.workflow.selectedItems()


        # TODO: Deal with children removal
        for obj in selected:

            index = self.workflow.indexOfTopLevelItem(obj)
            self.workflow.takeTopLevelItem(index)

    def runWorkflow(self):

        self.interfaces = plugm.availableInterfaces()

        self.runThread = runWorkflowThread(self.interfaces,self.workflow)
        self.runThread.start()


        # for itemIndex in range(self.workflow.topLevelItemCount()):
        #
        #     topLevelItem = self.workflow.topLevelItem(itemIndex)
        #
        #     if topLevelItem.childCount() > 0:
        #         print('Children to run!')
        #     else:
        #         print('trying to run')
        #         print('trying to run')
        #         self.workflow.itemWidget(topLevelItem, 0).extension.setInterfaces(self.interfaces)
        #        # runFunc = self.workflow.itemWidget(topLevelItem,0).extension.run
        #
        #         x = threading.Thread(target=self.workflow.itemWidget(topLevelItem,0).extension.run)
        #         x.start()



    def reject(self):
        print('rejected!')
        sys.exit(app.exec_())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.statusLabel.setText(_translate("MainWindow", "Status"))
        self.addButton.setText(_translate("MainWindow", "+"))
        self.removeButton.setText(_translate("MainWindow", "-"))
        self.runButton.setText(_translate("MainWindow", "Run"))
        self.cancelButton.setText(_translate("MainWindow", "Cancel"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))

