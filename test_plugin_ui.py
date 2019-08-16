
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(QtWidgets.QWidget):
    def __init__(self, name, parent=None):
        super(QtWidgets.QWidget, self).__init__(parent)

        self.widget = QtWidgets.QWidget()
        self.widget.setObjectName("widget")
        self.widget.setGeometry(QtCore.QRect(10,1,150, 58))
        self.grid = QtWidgets.QGridLayout(self.widget)

        self.buttonBox = QtWidgets.QDialogButtonBox(self.widget)
        self.buttonBox.setGeometry(QtCore.QRect(0, 0, 100, 10))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.grid.addWidget(self.buttonBox,0,0,1,1)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.setLayout(self.grid)
        print(self.sizeHint())

    def accept(self):
        print('accepted')

    def reject(self):
        print('rejected')

