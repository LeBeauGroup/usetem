import pluginTypes as pluginTypes
from PyQt5 import QtCore, QtGui, QtWidgets


class revSTEM(pluginTypes.IExtensionPlugin):

    def __init__(self):

        self.numFrames = 12
        self.binning = 8
        self.dwellTime = 0.5e-6

        self.detectorInfo = {'dwellTime': self.dwellTime, 'binning':self.binning, 'numFrames':self.numFrames,'names':['DF2','BF']}


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

        self.dwellTimeLabel = QtWidgets.QLabel(widget)
        self.dwellTimeLabel.setObjectName("dwellTimeLabel")

        formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.dwellTimeLabel)

        self.dwellTimelineEdit = QtWidgets.QLineEdit(widget)
        self.dwellTimelineEdit.setText(f'{self.dwellTime}')
        self.dwellTimelineEdit.setObjectName("dwellTimelineEdit")

        formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.dwellTimelineEdit)

        self.binningLabel = QtWidgets.QLabel(widget)
        self.binningLabel.setObjectName("binningLabel")

        formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.binningLabel)

        self.binningLineEdit = QtWidgets.QLineEdit(widget)
        self.binningLineEdit.setText(f'{self.binning}')
        self.binningLineEdit.setObjectName("binningLineEdit")

        formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.binningLineEdit)

        self.numberOfFramesLabel = QtWidgets.QLabel(widget)
        self.numberOfFramesLabel.setObjectName("numberOfFramesLabel")

        formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.numberOfFramesLabel)

        self.numberOfFramesLineEdit = QtWidgets.QLineEdit(widget)
        self.numberOfFramesLineEdit.setText(f'{self.numFrames}')
        self.numberOfFramesLineEdit.setObjectName("numberOfFramesLineEdit")

        formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.numberOfFramesLineEdit)

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
        self.dwellTimeLabel.setText(_translate("Dialog", "Dwell time"))
        self.binningLabel.setText(_translate("Dialog", "Binning"))
        self.numberOfFramesLabel.setText(_translate("Dialog", "Number of Frames"))

    def run(self):

        frames = int(self.numberOfFramesLineEdit.text())
        print(frames)
        tia = self.interfaces['tiascript']
        stem = tia.techniques['STEMImage']

        stem.setupAcquisition(self.detectorInfo)

        for i in range(frames):
            print(f'acqiuring {i}')
            rot = i*90
            stem.scanRotation(rot)
            stem.acquire()


    def reject(self):
        print('rejected')