

import sys
from PyQt5.QtWidgets import *

from PyQt5.uic import loadUi
from PyQt5.QtCore import QThread, pyqtSignal

from pumpFunctions import pumpy
from pumpFunctions.pumpAddress import pumpAdd
from pumpFunctions.pumpClient import pumpConn

from PyQt5.QtWidgets import QTabWidget
pumpMain = pumpConn("http://10.154.28.136:8000/pump")

# class MyThread(QThread):
#
#     signal = pyqtSignal('PyQt_PyObject')
#
#     def __init__(self):
#
#         QThread.__init__(self)

    #def run(self):




class usePump(QDialog):

    def __init__(self):

        super(usePump,self).__init__()

        loadUi('pump_design2.ui',self)

        self.setWindowTitle('usePump')

        #### For Tab Pump Connect
        self.radioButtonLocal.setChecked(True)

        self.lineEditIP.setText("http://10.154.28.136:8000/pump")

        self.pushButtonConnect.clicked.connect(self.pumpConnection)



    def pumpConnection(self):

        if self.radioButtonLocal.isChecked == True:

            pumpMain = pumpy.Pump(pumpAdd)

            self.labelMessage.setText('Pump is connected through Server')

        elif self.radioButtonServer.isChecked == True:

            pumpMain = pumpConn(self.lineEditIP.text())

            self.labelMessage.setText('Pump is connected Locally')

        else:

            self.labelMessage.setText('No Connection')










app = QApplication(sys.argv)

ex = usePump()
ex.show()
sys.exit(app.exec())
