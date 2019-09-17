
from PyQt5 import QtCore, QtGui, QtWidgets


class revSTEM(QtWidgets.QWidget):

    def __init__(self, name, plugins, parent=None):
        super(QtWidgets.QWidget, self).__init__(parent)

        self.numFrames = 12
        self.binning = 8
        self.dwellTime = 0.5e-6

        self.detectorInfo = {'dwellTime': self.dwellTime, 'binning':self.binning, 'numFrames':self.numFrames,'names':['DF2','BF']}
        self.plugins = plugins

        self.widget = QtWidgets.QWidget()
        self.widget.setObjectName("widget")
        self.widget.setGeometry(QtCore.QRect(10,1,150, 58))

        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")

        self.dwellTimeLabel = QtWidgets.QLabel(self.widget)
        self.dwellTimeLabel.setObjectName("dwellTimeLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.dwellTimeLabel)
        self.dwellTimelineEdit = QtWidgets.QLineEdit(self.widget)
        self.dwellTimelineEdit.setText(f'{self.dwellTime}')
        self.dwellTimelineEdit.setObjectName("dwellTimelineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.dwellTimelineEdit)

        self.binningLabel = QtWidgets.QLabel(self.widget)
        self.binningLabel.setObjectName("binningLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.binningLabel)
        self.binningLineEdit = QtWidgets.QLineEdit(self.widget)
        self.binningLineEdit.setText(f'{self.binning}')
        self.binningLineEdit.setObjectName("binningLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.binningLineEdit)

        self.numberOfFramesLabel = QtWidgets.QLabel(self.widget)
        self.numberOfFramesLabel.setObjectName("numberOfFramesLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.numberOfFramesLabel)
        self.numberOfFramesLineEdit = QtWidgets.QLineEdit(self.widget)
        self.numberOfFramesLineEdit.setText(f'{self.numFrames}')
        self.numberOfFramesLineEdit.setObjectName("numberOfFramesLineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.numberOfFramesLineEdit)

        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)

        self.retranslateUi(self.widget)

        QtCore.QMetaObject.connectSlotsByName(self)
        self.setLayout(self.gridLayout)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.dwellTimeLabel.setText(_translate("Dialog", "Dwell time"))
        self.binningLabel.setText(_translate("Dialog", "Binning"))
        self.numberOfFramesLabel.setText(_translate("Dialog", "Number of Frames"))

    def run(self):
        frames = int(self.numberOfFramesLineEdit.text())
        print(frames)
        tia = self.plugins['tiascript']
        stem = tia.techniques['STEMImage']

        stem.setupAcquisition(self.detectorInfo)

        for i in range(frames):
            print(f'acqiuring {i}')
            rot = i*90
            self.plugins['tiascript'].techniques['STEMImage'].scanRotation(rot)
            stem.acquire()


    def reject(self):
        print('rejected')