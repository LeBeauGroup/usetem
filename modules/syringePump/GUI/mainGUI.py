

import sys
from PyQt5.QtWidgets import *

from PyQt5.uic import loadUi
from PyQt5.QtCore import QThread, pyqtSignal

from pumpFunctions import pumpy
from pumpFunctions.pumpAddress import pumpAdd
from pumpFunctions.pumpClient import pumpConn

from PyQt5.QtWidgets import QTabWidget

from pumpFunctions import pumpCal

import numpy as np

ratioOH_FE = np.load('titration/ratioOH_FE.npy')
pHOH_FE = np.load('titration/pHOH_FE.npy')

ratioOH_FEAS = np.load('titration/ratioOH_FEAS.npy')
pHOH_FEAS = np.load('titration/pHOH_FEAS.npy')


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
        self.comboBoxInRate0.addItems(["ul/hr","ul/min","ul/sec","ml/hr","ml/min","ml/sec","nl/hr","nl/min","nl/sec","pl/hr","pl/min","pl/sec"])

        self.lineEditVolumeSet0.setText('5')
        self.comboBoxVolumeSetUnit0.addItems(["ml","ul","nl","pl"])

        self.lineEditTimeSet0.setText('5')
        self.comboBoxTimeSet0.addItems(["min","hr","sec"])


        ## for pump 1

        self.lineEditVolume1.setText('5')
        self.comboBoxVolUnit1.addItem("ml")

        self.lineEditInRate1.setText('5')
        self.comboBoxInRate1.addItems(["ul/hr","ul/min","ul/sec","ml/hr","ml/min","ml/sec","nl/hr","nl/min","nl/sec","pl/hr","pl/min","pl/sec"])

        self.lineEditVolumeSet1.setText('5')
        self.comboBoxVolumeSetUnit1.addItems(["ml","ul","nl","pl"])

        self.lineEditTimeSet1.setText('5')
        self.comboBoxTimeSet1.addItems(["min","hr","sec"])





        self.checkBoxPumpState0.setChecked(True)
        self.checkBoxPumpState1.setChecked(True)

        self.pushButtonStartPump.clicked.connect(self.pumpRun)
        self.pushButtonStopPump.clicked.connect(self.pumpStop)


        ### Rate calculator ###

        self.lineEditFe.setText('0.3')
        self.lineEditOH.setText('4.56')

        self.lineEditPhInt.setText('2.5')

        self.lineEditRatioReq.setText('15.2')

        self.lineEditRateTotal.setText('240')


        self.lineEditPumpFe.setText('0')

        self.lineEditPumpOH.setText('1')

        self.radioButtonUnitmMFe.setChecked(True)

        self.radioButtonUnitmMOH.setChecked(True)

        self.comboBoxRatetotalUnit.addItems(["ul/hr","ul/min","ul/sec","ml/hr","ml/min","ml/sec","nl/hr","nl/min","nl/sec","pl/hr","pl/min","pl/sec"])






        self.pushButtonRateCal.clicked.connect(self.rateCalculation)
        self.pushButtonRatePut.clicked.connect(self.putRateVal)



    def rateCalculation(self):

        if self.radioButtonUnitmMFe.isChecked() == True:
            factorFe = 3
        elif self.radioButtonUnituMFe.isChecked() == True:
            factorFe  = 6
        elif self.radioButtonUnitnMFe.isChecked() == True:
            factorFe = 9


        if self.radioButtonUnitmMOH.isChecked() == True:
            factorOH = 3
        elif self.radioButtonUnituMOH.isChecked() == True:
            factorOH  = 6
        elif self.radioButtonUnitnMOH.isChecked() == True:
            factorOH = 9



        param = dict()

        param['Fe'] = np.float(self.lineEditFe.text())*10**(-1*factorFe)
        param['OH'] = np.float(self.lineEditOH.text())*10**(-1*factorOH)

        param['initialpH'] = np.float(self.lineEditPhInt.text())

        rateFe,rateOH = pumpCal.pumpRate(param,np.float(self.lineEditRatioReq.text()),np.float(self.lineEditRateTotal.text()))

        ratio = np.around(np.float(self.lineEditRatioReq.text()),2)

        # if self.checkBoxpHAsCal.isChecked() == True:
        #
        #     tempNum = np.where(np.array(ratioOH_FEAS)==ratio)
        #
        #     self.lineEditpHCal.setText(str(np.around(pHOH_FEAS[tempNum[0][0]],2)))
        #
        # else:
        #
        #     tempNum = np.where(np.array(ratioOH_FE)==ratio)
        #
        #     self.lineEditpHCal.setText(str(np.around(pHOH_FE[tempNum[0][0]],2)))


        self.lineEditRateFe.setText(str(np.around(rateFe,2)))

        self.lineEditRateOH.setText(str(np.around(rateOH,2)))

    def putRateVal(self):

        self.comboBoxInRate0.setCurrentIndex(self.comboBoxRatetotalUnit.currentIndex())
        self.comboBoxInRate1.setCurrentIndex(self.comboBoxRatetotalUnit.currentIndex())

        if self.lineEditPumpFe.text()=='0':

            self.lineEditInRate0.setText(self.lineEditRateFe.text())

        else:

            self.lineEditInRate1.setText(self.lineEditRateFe.text())


        if self.lineEditPumpOH.text()=='1':

            self.lineEditInRate1.setText(self.lineEditRateOH.text())

        else:

            self.lineEditInRate0.setText(self.lineEditRateOH.text())









    def pumpRun(self):

        if self.checkBoxPumpState0.isChecked() == True:

            num =0

            self.pumpMain.FlowRate(self.lineEditInRate0.text(),self.comboBoxInRate0.currentText(),num)
            self.pumpMain.Volume(self.lineEditVolumeSet0.text(),self.comboBoxVolumeSetUnit0.currentText(),num)

            if self.comboBoxTimeSet0.currentText() == "sec":
                factorTime = 1
            elif self.comboBoxTimeSet0.currentText() == "min":

                factorTime = 60

            elif  self.comboBoxTimeSet0.currentText() == "hr":

                factorTime = 3600


            self.pumpMain.Time(str(np.float(self.lineEditTimeSet0.text())*factorTime),num)

            self.pumpMain.infuse(num)




        if self.checkBoxPumpState1.isChecked() == True:

            num=1

            self.pumpMain.FlowRate(self.lineEditInRate1.text(),self.comboBoxInRate1.currentText(),num)
            self.pumpMain.Volume(self.lineEditVolumeSet1.text(),self.comboBoxVolumeSetUnit1.currentText(),num)
            if self.comboBoxTimeSet1.currentText() == "sec":
                factorTime = 1
            elif self.comboBoxTimeSet1.currentText() == "min":

                factorTime = 60

            elif  self.comboBoxTimeSet1.currentText() == "hr":

                factorTime = 3600


            self.pumpMain.Time(str(np.float(self.lineEditTimeSet1.text())*factorTime),num)
            self.pumpMain.infuse(num)

    def pumpStop(self):

        if self.checkBoxPumpState0.isChecked() == True:

            num =0
            self.pumpMain.stop(num)

        if self.checkBoxPumpState1.isChecked() == True:

            num=1

            self.pumpMain.stop(num)




    def pumpConnection(self):

        if self.radioButtonLocal.isChecked() == True:

            self.pumpMain = pumpy.Pump(pumpAdd)

            self.labelMessage.setText('Pump is connected Locally')

        elif self.radioButtonServer.isChecked() == True:

            self.pumpMain = pumpConn(self.lineEditIP.text())

            self.labelMessage.setText('Pump is connected through Server')

        else:

            self.labelMessage.setText('No Connection')

        if self.pumpMain is None:

            self.labelMessage.setText('Connection Error')








app = QApplication(sys.argv)

ex = usePump()
ex.show()
sys.exit(app.exec())
