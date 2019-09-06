import useTEM.pluginManagement as plugm
import logging
import os
path = os.path.dirname(os.path.abspath(__file__))

import sys
from PyQt5.QtWidgets import QDialog, QApplication
from useTEM_ui import useTEMdialog

class AppWindow(QDialog):

    def __init__(self):
        super().__init__()
        self.ui = useTEMdialog()
        self.ui.setupUi(self, plugins)
        self.show()


if __name__ == '__main__':

	# loading the plugins
	plugins = plugm.availablePlugins()

	# launch the pyQt window
	app = QApplication(sys.argv)
	window = AppWindow()
	window.show()
	sys.exit(app.exec_())


