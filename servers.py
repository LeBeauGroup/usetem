import logging
import os

import sys
import multiprocessing
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QPushButton
from PyQt5.QtCore import QFile
from PyQt5 import uic
import subprocess
import threading

path = os.path.dirname(os.path.realpath(__file__))

# class ServerThread(threading.Thread):
# 	def __init__(self):
# 		self.stdout = None
# 		self.stderr = None
# 		threading.Thread.__init__(self)
#
# 	def run(self):
# 		p = subprocess.Popen(['python', 'servers/temscript_server.py'],
#                              shell=False,
#                              stdout=subprocess.PIPE)
#
# 		for stdout_line in iter(p.stdout.readline, ""):
# 			yield stdout_line
# 		p.stdout.close()
#
# 		return_code = p.wait()
#
# 		self.stdout, self.stderr = p.communicate()
#
# 	def print_stdout(self):
# 		print(self.stdout.readline)

isRunning = {'temscript': False, 'tiascript':False}
serverProcesses = {'temscript': None, 'tiascript':None}
def output_reader(proc):
    for line in iter(proc.stdout.readline, b''):
        print('got line: {0}'.format(line.decode('utf-8')), end='')


def startStopServer(name,button):


	if isRunning[name] is False:

		button.setStyleSheet("background-color: green")

		p = subprocess.Popen(['python', path+'/servers/'+name+'_server.py'],
							 shell=False,
							 stdout=subprocess.PIPE)

		t = threading.Thread(target=output_reader, args=(p,))
		t.start()
		serverProcesses[name] = p
		isRunning[name] = True

	elif isRunning[name] is True:

		serverProcesses[name].kill()
		isRunning[name] = False
		button.setStyleSheet("background-color:red")



if __name__ == '__main__':

	# launch the pyQt window
	app = QApplication(sys.argv)


	ui_file = QFile(path+'/servers/server.ui')
	ui_file.open(QFile.ReadOnly)

	window = uic.loadUi(ui_file)

	window.setWindowTitle('USETEM Local Servers')

	window.temscript.clicked.connect(lambda: startStopServer('temscript',window.temscript))
	window.tiascript.clicked.connect(lambda: startStopServer('tiascript',window.tiascript))
	#window.velow.clicked.connect(lambda: startServer('velow')
	window.show()

	app.setActiveWindow(window)


	sys.exit(app.exec_())


