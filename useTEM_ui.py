# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from extensions.revSTEM import revSTEM


class useTEMdialog(object):

    def setupUi(self, Dialog, plugins):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)

        #runButton = QtWidgets.QDialogButtonBox.Open
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Open)
        self.buttonBox.setObjectName("buttonBox")
        self.listWidget = QtWidgets.QTreeWidget(Dialog)
        self.listWidget.setColumnCount(1)
        self.listWidget.setGeometry(QtCore.QRect(10, 10, 371, 211))
        self.listWidget.setObjectName("listWidget")

        self.retranslateUi(Dialog)
        #self.listWidget.setExpanded(0,True);

        # setup plugin views
        #for plugin in plugins:

        print('setup widget')
        item = QtWidgets.QTreeWidgetItem(self.listWidget)

        item_widget = revSTEM('blash',plugins)
            #item.setSizeHint(QtCore.QSize(100,50))
        self.listWidget.addTopLevelItem(item)
        self.listWidget.setItemWidget(item,0,item_widget)

        self.buttonBox.accepted.connect(item_widget.run)
        self.buttonBox.rejected.connect(item_widget.reject)

        #QtCore.QMetaObject.connectSlotsByName(revSTEM)



       #  print('setup widget')
       #  item = QtWidgets.QTreeWidgetItem(self.listWidget)
       #  item_widget2 = test_plugin_ui2.Ui_Form('blash')
       # # item.setSizeHint(QtCore.QSize(100,50))
       #  self.listWidget.addTopLevelItem(item)
       #  self.listWidget.setItemWidget(item,0,item_widget2)

    def reject(self):
        print('rejected!')

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))

