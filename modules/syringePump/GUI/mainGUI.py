

import sys
from PyQt5.QtWidgets import *

from PyQt5.uic import loadUi
from PyQt5.QtCore import QThread, pyqtSignal

from pumpFunctions import pumpy
from pumpFunctions.pumpAddress import pumpAdd
from pumpFunctions.pumpClient import pumpConn

from PyQt5.QtWidgets import QTabWidget
# pumpMain = pumpConn("http://10.154.28.136:8000/pump")
# class MyThread(QThread):
#
#     signal = pyqtSignal('PyQt_PyObject')
#
#     def __init__(self):
#
#         QThread.__init__(self)

    #def run(self):

#pumpMain = pumpy.Pump(pumpAdd)

class usePump(QDialog):

    def __init__(self):

        super(usePump,self).__init__()

        loadUi('pump_design2.ui',self)

        self.setWindowTitle('usePump')

################ For Tab Pump Connect #################
        ## Defaults
        self.radioButtonLocal.setChecked(True)

        self.lineEditIP.setText("http://10.154.28.136:8000/pump")

        self.pushButtonConnect.clicked.connect(self.pumpConnection)





######### for tab pump settings #####
        ## Defaults

        self.checkBoxPump0.setChecked(True)
        self.checkBoxPump1.setChecked(True)

        ## for pump 0

        self.lineEditVolume0.setText('5')
        self.comboBoxVolUnit0.addItem("ml")

        self.lineEditInRate0.setText('5')
        self.comboBoxInRate0.addItems(["ml/hr","ml/min","ml/sec","ul/hr","ul/min","ul/sec","nl/hr","nl/min","nl/sec","pl/hr","pl/min","pl/sec"])

        self.lineEditVolumeSet0.setText('5')
        self.comboBoxVolumeSetUnit0.addItems(["ml","ul","nl","pl"])

        self.lineEditTimeSet0.setText('5')
        self.comboBoxTimeSet0.addItems(["sec"])


        ## for pump 1

        self.lineEditVolume1.setText('5')
        self.comboBoxVolUnit1.addItem("ml")

        self.lineEditInRate1.setText('5')
        self.comboBoxInRate1.addItems(["ml/hr","ml/min","ml/sec","ul/hr","ul/min","ul/sec","nl/hr","nl/min","nl/sec","pl/hr","pl/min","pl/sec"])

        self.lineEditVolumeSet1.setText('5')
        self.comboBoxVolumeSetUnit1.addItems(["ml","ul","nl","pl"])

        self.lineEditTimeSet1.setText('5')
        self.comboBoxTimeSet1.addItems(["sec"])





        self.checkBoxPumpState0.setChecked(True)
        self.checkBoxPumpState1.setChecked(True)

        self.pushButtonStartPump.clicked.connect(self.pumpRun)
        self.pushButtonStopPump.clicked.connect(self.pumpStop)



    def pumpRun(self,pumpMain):

        if self.checkBoxPumpState0.isChecked() == True:

            num =0

            pumpMain.FlowRate(self.lineEditInRate0.text(),self.lineEditInRate0.currentText(),num)
            pumpMain.Volume(self.lineEditVolumeSet0.text(),self.comboBoxVolumeSetUnit0.currentText(),num)
            pumpMain.Time(self.lineEditTimeSet0.text(),self.comboBoxTimeSet0.currentText(),num)

            pumpMain.infuse(num)




        if self.checkBoxPumpState1.isChecked() == True:

            num=1

            pumpMain.FlowRate(self.lineEditInRate1.text(),self.lineEditInRate1.currentText(),num)
            pumpMain.Volume(self.lineEditVolumeSet1.text(),self.comboBoxVolumeSetUnit1.currentText(),num)
            pumpMain.Time(self.lineEditTimeSet1.text(),self.comboBoxTimeSet1.currentText(),num)
            pumpMain.infuse(num)

    def pumpStop(self,pumpMain):

        if self.checkBoxPumpState0.isChecked() == True:

            num =0
            pumpMain.stop(num)

        if self.checkBoxPumpState1.isChecked() == True:

            num=1

            pumpMain.stop(num)




    def pumpConnection(self):

        if self.radioButtonLocal.isChecked() == True:

            pumpMain = pumpy.Pump(pumpAdd)

            self.labelMessage.setText('Pump is connected Locally')

        elif self.radioButtonServer.isChecked() == True:

            pumpMain = pumpConn(self.lineEditIP.text())

            self.labelMessage.setText('Pump is connected through Server')

        else:

            self.labelMessage.setText('No Connection')

        if pumpMain is None:

            self.labelMessage.setText('Connection Error')








app = QApplication(sys.argv)

ex = usePump()
ex.show()
sys.exit(app.exec())
