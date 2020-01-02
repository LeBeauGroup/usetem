from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import  Qt
import sys
import comtypes.client as ct
from comtypes.gen.IOMLib import _99A162A6_3022_4B64_88C3_A62A6BE22239_0_1_0 as iom

class Example(QtWidgets.QWidget):

	def __init__(self):
		super().__init__()

		self.isXMoving = False
		self.stageVelocity = 10e-9


		tem2 = ct.CreateObject('Fei.Tem.Instrument2Connection.1')
		tem2.Connect()

		tem3 = ct.CreateObject('Fei.Tem.Instrument3Connection.1')
		tem3.Connect()

		self.instr2 = tem2.Instrument
		self.instr3 = tem3.Instrument


		self.instr2.Column.Stage.Enable()

		self.initUI()
		self.modes = dict()
		self.modes['defocus'] = {'step':0.5e-9}
		self.currentMode = 'defocus'

	def changeDefocus(self, step:float):
		self.instr3.Column.Optics.defocus += step
		print(self.instr3.Column.Optics.defocus)

	def startJogStage(self, axis, direction):
		#self.instr2.Column.Stage.Enable()
		# self.instr2.Column.Stage.MeasurePosition()
		#newPos = self.instr2.Column.Stage.Position
		#newPos.x += 10e-9*direction
		self.instr2.Column.Stage.startJoggingAxis(axis, self.stageVelocity*direction)
		#self.instr2.Column.Stage.moveWithSpeed(newPos, iom.enStageAxis_x,100e-9)

	def stopJogStage(self, axis):
		# self.instr2.Column.Stage.MeasurePosition()
		#newPos = self.instr2.Column.Stage.Position
		#newPos.x += 10e-9*direction
		self.instr2.Column.Stage.stopJoggingAxis(axis)
		#self.instr2.Column.Stage.moveWithSpeed(newPos, iom.enStageAxis_x,100e-9)


	def changeValue(self,sign:int):

		step = self.modes[self.currentMode]['step']
		mode = self.currentMode
		if mode == 'defocus':
			self.changeDefocus(step*sign)


	def changeStep(self, factor):

		if factor > 0:
			newStep = self.modes[self.currentMode]['step'] * factor
		elif factor < 0:
			newStep = self.modes[self.currentMode]['step'] / (-1*factor)


		print(f'{self.currentMode} step size is now {newStep}')
		self.modes[self.currentMode]['step'] = newStep

	def keyReleaseEvent(self, e):

		if e.isAutoRepeat():
			e.ignore()
			return

		if self.currentMode == 'stage':

			print('release stage')
			if e.key() == Qt.Key_Left or e.key() == Qt.Key_Right:
				if self.isXMoving:
					self.stopJogStage(iom.enStageAxis_x)
					self.isXMoving = False
					print('stop moving')


	def keyPressEvent(self, e):

		if self.currentMode == 'stage':
			if e.key() == Qt.Key_Left:
				if not self.isXMoving:
					print('start moving')
					self.startJogStage(iom.enStageAxis_x, -1)
					self.isXMoving = True

			elif e.key() == Qt.Key_Right:
				if not self.isXMoving:
					print('start moving')
					self.startJogStage(iom.enStageAxis_x, 1)
					self.isXMoving = True

			elif e.key() == Qt.Key_Up:
				self.stageVelocity *= 1.5
			elif e.key() == Qt.Key_Down:
				self.stageVelocity  *= 1.5
		else:

			if e.key() == Qt.Key_Left:
				self.changeValue(-1)
			elif e.key() == Qt.Key_Right:
				self.changeValue(+1)


			elif e.key() == Qt.Key_Up:
				self.changeStep(1.5)
			elif e.key() == Qt.Key_Down:
				self.changeStep(-1.5)

			elif e.key() == Qt.Key_D:
				self.currentMode = 'defocus'
			elif e.key() == Qt.Key_S:
				self.currentMode = 'stage'

	def initUI(self):
		self.setGeometry(300, 300, 300, 220)
		self.setWindowTitle('Icon')
		self.setWindowIcon(QtGui.QIcon('web.png'))

		self.show()

def main():

    app = QApplication(sys.argv)
    w = Example()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()