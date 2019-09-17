import useTEM.pluginManagement as plugm
import logging
import os
path = os.path.dirname(os.path.abspath(__file__))

import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5 import QtGui
from useTEM_ui import UseTEMUI


if __name__ == '__main__':

	# loading the plugins
	plugins = plugm.availableExtensions()

	# launch the pyQt window
	app = QApplication(sys.argv)
	mainWindow = QMainWindow()

	app.setActiveWindow(mainWindow)


	ui = UseTEMUI()
	ui.setupUi(mainWindow,plugins)
	mainWindow.show()
	sys.exit(app.exec_())


