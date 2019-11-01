import useTEM.pluginManagement as plugm
import logging
import os
path = os.path.dirname(os.path.abspath(__file__))

import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, Qt, QtWidgets

from PyQt5.QtCore import pyqtSlot

from useTEM_ui import UseTEMUI
from PyQt5.Qt import QFile
from PyQt5 import uic
import copy

class WorkflowItem(QtWidgets.QTreeWidgetItem):

	@pyqtSlot(str, str)
	def updateItemData(self, key, value):
		# print(self.sender())
		test = self.sender()

		# key = objectName.replace('Edit', '')
		# self.data[key] = value
		# print(key,value)
		# print(self.data)


class WorkflowThread(QtCore.QThread):

	def __init__(self, interfaces, workflow, plugins):
		"""
		Make a new thread instance with the specified
	   workflow from UI.



		:param subreddits: A list of subreddit names
		:type subreddits: list
		"""

		super().__init__()
		print('launched')


		self.interfaces = interfaces
		self.workflow = workflow
		self.plugins = plugins



	def __del__(self):
		self.wait()

	def run(self):

		for itemIndex in range(self.workflow.topLevelItemCount()):

			topLevelItem = self.workflow.topLevelItem(itemIndex)

			if topLevelItem.childCount() > 0:
				print('Children to run!')
			else:
				print('got here')
				itemData = topLevelItem.data
				plugin = self.plugins[itemData['name']]

				plugin.setInterfaces(self.interfaces)
				result = plugin.run(itemData)


				# result = self.workflow.itemWidget(topLevelItem, 0).extension.run()



class USETEMGuiManager():
	ui = None

	def __init__(self, ui, plugs):

		self.ui = ui
		self.plugins = plugs

		self.ui.addButton.clicked.connect(self.addToWorkflow)
		self.ui.abortButton.clicked.connect(self.killWorkflow)

		workflowTree = self.ui.workflowTree
		workflowTree.plugins = plugs

		if isinstance(workflowTree, QtWidgets.QTreeWidget):

			workflowTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
			workflowTree.customContextMenuRequested.connect(self.prepareMenu)

		workflowTree.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
		# plugsTree.setSelectionMode(QtCore.Qt.QAbstractItemView::ExtendedSelection);
		workflowTree.setDragEnabled(True)
		workflowTree.setAcceptDrops(True)
		workflowTree.setDropIndicatorShown(True)
		workflowTree.setAnimated(True)
		workflowTree.doubleClicked.connect(self.addToWorkflow)

	# def selectionChanged(self):
	#
	# 	model = self.ui.pluginsTree.model()
	#
	# 	for ind in self.ui.pluginsTree.selectedIndexes():
	# 		print(ind.row())
	# 		# item = model.itemFromIndex(ind)
	# 		# self.ui.usetem_widget.setWidget(item.data())

	def prepareMenu(self, point):

		newMenu = QtWidgets.QMenu(self.ui)

		removeAct = QtWidgets.QAction(QtGui.QIcon(), '&Remove Workflow Item', self.ui)

		removeAct.triggered.connect(self.removeWorkflowItem)
		newMenu.addAction(removeAct)



		newMenu.exec(self.ui.workflowTree.mapToGlobal(point))

	def removeWorkflowItem(self):

		currentItem = self.ui.workflowTree.currentItem()
		currentIndex = self.ui.workflowTree.indexOfTopLevelItem(currentItem)
		self.ui.workflowTree.takeTopLevelItem(currentIndex)

	def addToWorkflow(self):

		selected = self.ui.availablePlugins.selectedItems()

		for obj in selected:
			label = self.ui.availablePlugins.itemWidget(obj, 0)
			self.addItem(label.text())

	# self.workflow.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
	def addItem(self, name):

		workflowTree = self.ui.workflowTree
		item = WorkflowItem(workflowTree)
		# use for iterable items | QtCore.Qt.ItemIsDropEnabled
		union = QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled

		item.setFlags(union)

		item.data = copy.copy(self.plugins[name].defaultParameters)
		item_widget = self.plugins[name].ui(item)

		workflowTree.addTopLevelItem(item)

		workflowTree.setItemWidget(item, 0, item_widget)

	def setupPlugins(self):

		plugsTree = self.ui.availablePlugins


		for key in self.plugins:
			new_item = QtWidgets.QTreeWidgetItem(plugsTree)

			pluginItem = QtWidgets.QLabel()
			pluginItem.setText(key)

			plugsTree.addTopLevelItem(new_item)
			plugsTree.setItemWidget(new_item, 0, pluginItem)

		plugsTree.doubleClicked.connect(self.addToWorkflow)


	def runWorkflow(self):

		self.interfaces = plugm.availableInterfaces()
		self.runThread = WorkflowThread(self.interfaces, self.ui.workflowTree, self.plugins)
		self.runThread.start()

	def killWorkflow(self):

		if isinstance(self.runThread, WorkflowThread):
			self.runThread.terminate()


if __name__ == '__main__':

	# loading the plugins
	plugins = plugm.availableExtensions()

	# launch the pyQt window
	app = QApplication(sys.argv)

	ui_file = QFile("mainWindow.ui")
	ui_file.open(QFile.ReadOnly)

	window = uic.loadUi(ui_file)

	guiManager = USETEMGuiManager(window,plugins)
	guiManager.setupPlugins()

	window.runButton.clicked.connect(guiManager.runWorkflow)

	# window.pluginsTree.selectionChanged()

	window.setWindowTitle('USETEM Workflow')
	# mainWindow = QMainWindow()
	# mainWindow.setWindowTitle('USE-TEM')




	# app.setActiveWindow(mainWindow)

	# ui = UseTEMUI()
	# ui.setupUi(mainWindow,plugins)

	window.show()
	sys.exit(app.exec_())


