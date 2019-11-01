import pluginTypes as pluginTypes
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import os


class revSTEM(pluginTypes.IExtensionPlugin):

	def __init__(self):

		self.uiPath = os.path.dirname(os.path.realpath(__file__))
		self.uiFile = QtCore.QFile('revSTEM.ui')
		self.uiFile.open(QtCore.QFile.ReadOnly)

		self.numFrames = 12
		self.binning = '512x512'
		self.dwellTime = 0.5e-6

		# self.detectorInfo = {'dwellTime': self.dwellTime, 'binning': self.binning, 'numFrames': self.numFrames,
		# 					 'detectors': ['DF2', 'BF']}

		self.defaultParameters = {'name': 'revSTEM', 'rotation': 90, 'dwellTime': self.dwellTime,
		                          'binning': self.binning,
		                          'numFrames': self.numFrames, 'detectors': ['HAADF']}

	def setInterfaces(self, interfaces):
		self.interfaces = interfaces

	def ui(self, item, parent=None):

		def updateItemData():

			sender = widget.sender()
			senderName = sender.objectName()

			if "Edit" in senderName:
				key = senderName.replace('Edit', '')

				if isinstance(sender, QtWidgets.QLineEdit):
					widget.item.data[key] = sender.text()

				elif isinstance(sender, QtWidgets.QListWidget):
					newSelection = list()

					for selectedItem in sender.selectedItems():
						text = selectedItem.text()
						newSelection.append(text)

					widget.item.data[key] = newSelection

				elif isinstance(sender, QtWidgets.QComboBox):
					widget.item.data[key] = sender.currentText()

		path = self.uiPath + '\\revSTEM.ui'
		widget: QtWidgets = uic.loadUi(path, parent)
		item.setSizeHint(0, widget.size())
		widget.item = item

		for child in widget.children():
			name = child.objectName()

			if "Edit" in name:

				parameterName = name.replace('Edit', '')

				if isinstance(child, QtWidgets.QListWidget):

					for it in range(0, child.count()):

						rowItem = child.item(it)
						label = rowItem.text()

						if label in item.data[parameterName]:
							rowItem.setSelected(True)
						else:
							rowItem.setSelected(False)

					child.itemSelectionChanged.connect(updateItemData)

				elif isinstance(child, QtWidgets.QLineEdit):
					child.setText(f'{item.data[parameterName]}')
					child.editingFinished.connect(updateItemData)

				elif isinstance(child, QtWidgets.QComboBox):
					paramValue = item.data[parameterName]
					for ind in range(0, child.count()):

						if child.itemText(ind) == str(paramValue):
							child.setCurrentIndex(ind)
							break
					child.currentIndexChanged.connect(updateItemData)

		return widget

	def retranslateUi(self, widget):
		_translate = QtCore.QCoreApplication.translate
		widget.setWindowTitle(_translate("Dialog", "Dialog"))
		self.dwellTimeLabel.setText(_translate("Dialog", "Dwell time"))
		self.binningLabel.setText(_translate("Dialog", "Binning"))
		self.numberOfFramesLabel.setText(_translate("Dialog", "Number of Frames"))

	def run(self, input):

		frames = int(input['numFrames'])
		print(frames)
		tia = self.interfaces['tiascript']
		stem = tia.techniques['STEMImage']

		stem.setupAcquisition(input)
		rotAngle = input['rotation']

		for i in range(frames):
			print(f'acqiuring {i}')
			rot = i * rotAngle
			stem.scanRotation(rot)
			stem.acquire()

	def reject(self):
		print('rejected')
