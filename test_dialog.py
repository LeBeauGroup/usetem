# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import test_plugin_ui
import test_plugin_ui2


class Ui_Dialog(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.listWidget = QtWidgets.QTreeWidget(Dialog)
        self.listWidget.setColumnCount(1)
        self.listWidget.setGeometry(QtCore.QRect(10, 10, 371, 211))
        self.listWidget.setObjectName("listWidget")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        #self.listWidget.setExpanded(0,True);

        for i in range(2):
            print('setup widget')
            item = QtWidgets.QTreeWidgetItem(self.listWidget)
            item_widget = test_plugin_ui.Ui_Form('blash')
            #item.setSizeHint(QtCore.QSize(100,50))
            self.listWidget.addTopLevelItem(item)

            item2 = QtWidgets.QTreeWidgetItem(item)
            item_widget2 = test_plugin_ui2.Ui_Form('blash')

            # item.setSizeHint(QtCore.QSize(100,50))

            self.listWidget.setItemWidget(item,0,item_widget)
            self.listWidget.setItemWidget(item2, 0, item_widget2)

            item.addChild(item2)


       #  print('setup widget')
       #  item = QtWidgets.QTreeWidgetItem(self.listWidget)
       #  item_widget2 = test_plugin_ui2.Ui_Form('blash')
       # # item.setSizeHint(QtCore.QSize(100,50))
       #  self.listWidget.addTopLevelItem(item)
       #  self.listWidget.setItemWidget(item,0,item_widget2)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))

