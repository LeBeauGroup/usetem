import pluginTypes as pluginTypes
from PyQt5 import QtCore, QtGui, QtWidgets


class forLoop(pluginTypes.IExtensionPlugin):

    # def __init__(self):
    #
    #     pass

    def setInterfaces(self, interfaces):
        self.interfaces = interfaces


    def ui(self):

        widget = QtWidgets.QWidget()
        widget.setObjectName("widget")
        widget.setGeometry(QtCore.QRect(10,1,150, 58))

        gridLayout = QtWidgets.QGridLayout(widget)
        gridLayout.setObjectName("gridLayout")
        formLayout = QtWidgets.QFormLayout()
        formLayout.setObjectName("formLayout")

        self.loopLabel = QtWidgets.QLabel(widget)
        self.loopLabel.setObjectName("Loop Label")

        formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.loopLabel)

        self.dwellTimelineEdit = QtWidgets.QLineEdit(widget)
        self.dwellTimelineEdit.setText(f'1')
        self.dwellTimelineEdit.setObjectName("dwellTimelineEdit")

        formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.dwellTimelineEdit)


        gridLayout.addLayout(formLayout, 0, 0, 1, 1)

        # QtCore.QMetaObject.connectSlotsByName(self)

        widget.setLayout(gridLayout)
        self.retranslateUi(widget)
        widget.extension = self
        self.ui = widget


        return self.ui


    def retranslateUi(self,widget):
        _translate = QtCore.QCoreApplication.translate
        widget.setWindowTitle(_translate("Dialog", "Dialog"))
        self.loopLabel.setText(_translate("Dialog", "Repeat Count"))

    def run(self):

        print(self.ui.children())


    def reject(self):
        print('rejected')