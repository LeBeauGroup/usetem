import useTEM.pluginManagement as plugm
import logging
import os
import numpy as np
path = os.path.dirname(os.path.realpath(__file__))

import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, Qt, QtWidgets

from PyQt5.Qt import QFile
from PyQt5 import uic
import copy

class WorkflowItem(QtWidgets.QTreeWidgetItem):
	pass
	# @pyqtSlot(str, str)
	# def updateItemData(self, key, value):
	# 	# print(self.sender())
	# 	test = self.sender()
	#
	# 	# key = objectName.replace('Edit', '')
	# 	# self.data[key] = value
	# 	# print(key,value)
	# 	# print(self.data)


class WorkflowThread(QtCore.QThread):

	currentWorkflowItemDidChange = QtCore.pyqtSignal(WorkflowItem)
	workflowItemNeedsUpdate = QtCore.pyqtSignal(WorkflowItem)

	def __init__(self, interfaces, workflow, plugins):
		"""
		Make a new thread instance with the specified
	   workflow from UI.



		:param subreddits: A list of subreddit names
		:type subreddits: list
		"""
		super().__init__()
		self.interfaces = interfaces
		self.workflow = workflow
		self.plugins = plugins

	def __del__(self):
		self.wait()

	def run(self):

		def execute(runItem):

			itemData = runItem.data
			plugin = self.plugins[itemData['name']]
			pluginName = itemData['name']

			plugin.setInterfaces(self.interfaces)

			if runItem.childCount() > 0:

				loopParameters = runItem.data
				loopValues = plugin.run(loopParameters)

				for value in loopValues:
					for ind in range(runItem.childCount()):
						childToRun = runItem.child(ind)

						if not loopParameters['variableName'] == 'None':
							variableName = loopParameters['variableName']

							if variableName in list(childToRun.data.keys()):

								oldData = childToRun.data[variableName]

								if isinstance(oldData, str):
									childToRun.data[variableName] = str(value)
								elif isinstance(oldData, list):
									childToRun.data[variableName] = [value]

								self.workflowItemNeedsUpdate.emit(childToRun)

							else:
								pass

							self.currentWorkflowItemDidChange.emit(childToRun)
							execute(childToRun)
			else:

				result = plugin.run(itemData)
			return

		result = None


		for itemIndex in range(self.workflow.topLevelItemCount()):

			topLevelItem = self.workflow.topLevelItem(itemIndex)

			itemToRun = topLevelItem
			self.currentWorkflowItemDidChange.emit(itemToRun)
			result = execute(itemToRun)

def updateWorkflow(item):
	print(item)

class USETEMGuiManager:
	ui = None

	def __init__(self, ui, plugs):

		self.ui = ui
		self.plugins = plugs

#		self.ui.addButton.clicked.connect(self.addToWorkflow)
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



	def prepareMenu(self, point):

		newMenu = QtWidgets.QMenu(self.ui)

		# setup menu items
		duplicateAct = QtWidgets.QAction(QtGui.QIcon(), '&Duplicate Workflow Item', self.ui)
		removeAct = QtWidgets.QAction(QtGui.QIcon(), '&Remove Workflow Item', self.ui)

		# Connect them up to methods
		duplicateAct.triggered.connect(self.duplicateWorkflowItem)
		removeAct.triggered.connect(self.removeWorkflowItem)

		newMenu.addAction(duplicateAct)
		newMenu.addAction(removeAct)

		point.setY(point.y() + 30)
		newMenu.exec(self.ui.workflowTree.mapToGlobal(point))

	def duplicateWorkflowItem(self):
		print('Implement duplicating items')

		# TODO: Duplicate below current item

	def removeWorkflowItem(self):
		# TODO: Implement dealing with selected child items

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

		item.data = copy.copy(self.plugins[name].defaultParameters)
		item_widget = self.plugins[name].ui(item)

		if self.plugins[name].acceptsChildren is True:
			union = union | QtCore.Qt.ItemIsDropEnabled

		item.setFlags(union)

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


	def selectWorkflowItem(self,item):
		workflowTree:QtWidgets.QTreeWidget = self.ui.workflowTree
		workflowTree.setCurrentItem(item)

	def updateWorkflowItem(self, item):
		workflowTree: QtWidgets.QTreeWidget = self.ui.workflowTree

		itemData = item.data
		updatedWidget = self.plugins[itemData['name']].ui(item)

		workflowTree.setItemWidget(item, 0, updatedWidget)

	def runWorkflow(self):

		self.interfaces = plugm.availableInterfaces()

		self.runThread = WorkflowThread(self.interfaces, self.ui.workflowTree, self.plugins)

		self.runThread.currentWorkflowItemDidChange.connect(self.selectWorkflowItem)
		self.runThread.workflowItemNeedsUpdate.connect(self.updateWorkflowItem)
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

	p = window.palette()
	p.setColor(QtGui.QPalette.Highlight, QtGui.QColor('gray'))
	window.setPalette(p)

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


