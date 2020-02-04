# Universal Scripting Engine for Transmission Electron Microscopy
# A framework to automate electron microscopy data collection
# Copyright (C) 2020 James M. LeBeau

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License 
# a long with this program.  If not, see <https://www.gnu.org/licenses/>.

from useTEM import pluginManagement as plugm
import logging
import os
path = os.path.dirname(os.path.realpath(__file__))

import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.Qt import QFile
from PyQt5 import uic
import copy
import json
import bibtexparser
import re
import types
from useTEM.workflowThread import WorkflowThread, WorkflowItem


def updateWorkflow(item):
	print(item)

class USETEMGuiManager(QtCore.QObject):
	ui = None

	keyArrowPressed = QtCore.pyqtSignal()

	def __init__(self, ui, plugs):
		super(USETEMGuiManager, self).__init__()
		self.ui = ui
		self.plugins = plugs



		self.ui.actionSave_Workflow.triggered.connect(self.saveWorkflow)
		self.ui.actionOpen_Workflow.triggered.connect(self.loadWorkflow)
		self.ui.actionRun_Workflow.triggered.connect(self.runWorkflow)
		self.ui.actionCitations.triggered.connect(self.generate_citations)

		self.ui.actionSave_Workflow.setShortcut('Ctrl+S')
		self.ui.actionOpen_Workflow.setShortcut('Ctrl+O')
		self.ui.actionRun_Workflow.setShortcut('Ctrl+R')

		workflowTree = self.ui.workflowTree
		workflowTree.plugins = plugs

		self.ui.actionClearWorkflow.triggered.connect(workflowTree.clear)


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

		currentItem = self.ui.workflowTree.currentItem()
		parent = currentItem.parent()

		# if parent is None:
		self.addItem(currentItem.data['name'],parent, copy.deepcopy(currentItem.data))
		# else:
		# 	parent.removeChild(currentItem)

	def removeWorkflowItem(self):

		currentItem = self.ui.workflowTree.currentItem()

		parent = currentItem.parent()

		if parent is None:
			currentIndex = self.ui.workflowTree.indexOfTopLevelItem(currentItem)
			self.ui.workflowTree.takeTopLevelItem(currentIndex)
		else:

			if currentItem.data['name'] in ['elseIf', 'else']:
				currentIndex = parent.indexOfChild(currentItem)
				parent.data['conditions'].pop(currentIndex)
				print(parent.data)

			parent.removeChild(currentItem)


	def alert(self, title, message):
		QtWidgets.QMessageBox.about(window, title, message)

	def addToWorkflow(self):


		selected = self.ui.availablePlugins.selectedItems()

		for item in selected:

			if callable(item.data):
				continue
			else:
				nameOfPlugin = item.data
				self.addItem(nameOfPlugin)

	# self.workflow.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
	def addItem(self, name, parent:QtWidgets.QTreeWidgetItem=None, data=None):

		workflowTree = self.ui.workflowTree
		item = WorkflowItem(parent)
		# use for iterable items | QtCore.Qt.ItemIsDropEnabled
		union = QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled

		if data is None:
			item.data = copy.copy(self.plugins[name].defaultParameters)
		else:
			item.data = copy.copy(data)



		item_widget = self.plugins[name].ui(item)

		if self.plugins[name].acceptsChildren is True:
			union = union | QtCore.Qt.ItemIsDropEnabled


		item.setFlags(union)

		# cleanup children from item, do not need to use this from loading
		# try:
		# 	del item.data["children"]
		# except KeyError:
		# 	print("Key 'children' not found")

		if parent is None:
			workflowTree.addTopLevelItem(item)
		else:
			parent.addChild(item)
			parent.setExpanded(True)



		workflowTree.setItemWidget(item, 0, item_widget)

		if name == 'conditional':
			print('click')
			item_widget.findChild(QtWidgets.QWidget, 'widget').addElseIf.click()

		return item


	def setupPlugins(self):

		plugsTree :QtWidgets.QTreeWidget = self.ui.availablePlugins

		for key in self.plugins:

			displayName = self.plugins[key].displayName
			category = self.plugins[key].category
			toolTip = self.plugins[key].description

			categoryItem = None

			if category is not None:
				topLevelCount = plugsTree.topLevelItemCount()

				if topLevelCount == 0:
					categoryItem = QtWidgets.QTreeWidgetItem(0)
					categoryItem.setText(0, category)
					plugsTree.addTopLevelItem(categoryItem)

				else:

					for ind in range(topLevelCount):
						topLevelItem = plugsTree.topLevelItem(ind)

						if topLevelItem.text(0) == category:
							categoryItem = topLevelItem
							break

					if categoryItem is None:
						categoryItem = QtWidgets.QTreeWidgetItem(0)
						categoryItem.setText(0, category)
						plugsTree.addTopLevelItem(categoryItem)


			pluginItem = QtWidgets.QTreeWidgetItem(0)

			pluginItem.setText(0, displayName)
			pluginItem.data = key
			pluginItem.setToolTip(0,toolTip)

			if category is not None:
				categoryItem.addChild(pluginItem)
				# plugsTree.setItemWidget(new_item, 0, pluginItem)
			else:
				plugsTree.addTopLevelItem(pluginItem)
				# plugsTree.setItemWidget(new_item, 0, pluginItem)

		plugsTree.doubleClicked.connect(self.addToWorkflow)
		plugsTree.expandAll()


	def selectWorkflowItem(self,item):

		workflowTree:QtWidgets.QTreeWidget = self.ui.workflowTree

		workflowTree.setCurrentItem(item)
		workflowTree.itemWidget(item, 0).setFocus()



	def updateWorkflowItem(self, item):
		workflowTree: QtWidgets.QTreeWidget = self.ui.workflowTree

		itemData = item.data
		updatedWidget = self.plugins[itemData['name']].ui(item)

		workflowTree.setItemWidget(item, 0, updatedWidget)
		self.selectWorkflowItem(item)


	def workflowFinished(self):

		runButton:QtWidgets.QPushButton = self.ui.runButton

		runButton.setText('Run')
		runButton.clicked.disconnect()
		runButton.clicked.connect(self.runWorkflow)


	def runWorkflow(self):

		self.interfaces = plugm.availableInterfaces()
		print(self.interfaces)

		self.runThread = WorkflowThread(self.interfaces, self.ui.workflowTree, self.plugins)

		self.runThread.currentWorkflowItemDidChange.connect(self.selectWorkflowItem)
		self.runThread.workflowItemNeedsUpdate.connect(self.updateWorkflowItem)
		self.runThread.workflowFinished.connect(self.workflowFinished)
		self.runThread.workflowConditionalFailed.connect(self.alert)

		self.ui.runButton.setText('Abort')

		try:
			self.ui.runButton.clicked.disconnect()
		except Exception:
			pass

		self.ui.runButton.clicked.connect(self.killWorkflow)

		try:
			self.runThread.start()
		except Exception as e:
			print(e)

	def killWorkflow(self):

		if isinstance(self.runThread, WorkflowThread):
			self.runThread.terminate()

			try:
				self.ui.runButton.clicked.disconnect()
				self.ui.runButton.clicked.connect(self.runWorkflow)
				self.ui.runButton.setText('Run')

			except Exception:
				pass




	def saveWorkflow(self):

		name = QtWidgets.QFileDialog.getSaveFileName(self.ui, 'Save File','untitled.usetem')[0]

		if name is '':
			return

		workflowTree:QtWidgets.QTreeWidget =  self.ui.workflowTree

		workflow = {}
		workflow['items'] = []

		# function to save items recursively

		def prepareJSONChild(itemToPrepare):

			itemDict = itemToPrepare.data

			if itemToPrepare.childCount() > 0:

				dictWithChildren = itemDict
				dictWithChildren.update({'children': []})

				for ind in range(itemToPrepare.childCount()):

					childToPrepare = itemToPrepare.child(ind)
					itemDict['children'].append(childToPrepare.data)

					prepareJSONChild(childToPrepare)

			return itemDict

		# for each item in the tree, test if it has children and prepare data accordingly
		for ind in range(workflowTree.topLevelItemCount()):

			item = workflowTree.topLevelItem(ind)

			if item.childCount() > 0:

				workflow['items'].append(prepareJSONChild(item))
			else:
				workflow['items'].append(item.data)


		with open(name, 'w') as outfile:
			json.dump(workflow, outfile,indent=4)

	def loadWorkflow(self):


		name = QtWidgets.QFileDialog.getOpenFileName(self.ui, 'Open File')[0]

		if name is '':
			return

		workflowTree:QtWidgets.QTreeWidget =  self.ui.workflowTree

		workflowTree.clear()

		with open(name) as json_file:
			workflow = json.load(json_file)


			def restoreItem(itemToAdd, parent=None,childIndex=0):

				if parent is None:
					newParent = self.addItem(itemToAdd['name'], data=itemToAdd)

					if 'children' in itemToAdd.keys():
						for index, child in enumerate(item['children']):
							restoreItem(child, newParent,index)

				elif parent is not None:

					parentWidget = workflowTree.itemWidget(parent, 0).findChild(QtWidgets.QWidget, 'widget')

					if itemToAdd['name'] == 'elseIf':

						if childIndex > 0:
							parentWidget.addElseIf.click()

						if 'children' in itemToAdd.keys():

							for index, child in enumerate(itemToAdd['children']):
								restoreItem(child, parent.child(childIndex),index)

					elif itemToAdd['name'] =='else':
						parentWidget.addElse.click()

						if 'children' in itemToAdd.keys():

							for index, child in enumerate(itemToAdd['children']):
								restoreItem(child, parent.child(childIndex),index)

					else:
						newParent = self.addItem(itemToAdd['name'], parent=parent, data=itemToAdd)

						if 'children' in itemToAdd.keys():
							print(itemToAdd.keys())

							for indx, child in enumerate(itemToAdd['children']):
								print(indx)
								restoreItem(child, newParent, indx)



			for item in workflow['items']:
				restoreItem(item)
				# treeItem.setText(0, item['name'])


	def generate_citations(self):

		saveLocation = QtWidgets.QFileDialog.getSaveFileName(self.ui, 'Save Bibtex file', 'untitled.bib')[0]

		if saveLocation is '':
			return

		def grab_childCitation(checkItem):
			name = checkItem.data['name']
			thePlugin = self.plugins[name]
			itemBib = thePlugin.citations()

			if itemBib is not None:
				for bibItem in itemBib.entries:
					theBib.entries.append(bibItem)

			if checkItem.childCount() > 0:

				for ind in range(checkItem.childCount()):
					childToCheck = checkItem.child(ind)
					grab_childCitation(childToCheck)


		theBib = bibtexparser.bibdatabase.BibDatabase()
		workflow = self.ui.workflowTree

		for itemIndex in range(workflow.topLevelItemCount()):
			itemToCheck = workflow.topLevelItem(itemIndex)

			grab_childCitation(itemToCheck)

		writer = bibtexparser.bwriter.BibTexWriter()

		# to clean duplicates, use dict
		dupFreeBib = bibtexparser.bibdatabase.BibDatabase()
		entriesDict = theBib.entries_dict
		for key in entriesDict:
			dupFreeBib.entries.append(entriesDict[key])

		with open(saveLocation, 'w') as bibfile:
			bibfile.write(writer.write(dupFreeBib))






if __name__ == '__main__':

	# loading the plugins
	plugins = plugm.availableExtensions()

	# launch the pyQt window
	app = QApplication(sys.argv)

	ui_file = QFile(path+"\mainWindow.ui")
	ui_file.open(QFile.ReadOnly)

	window = uic.loadUi(ui_file)


	# def patch(target):
	# 	def keyPressEvent(target, event):
	# 		guiManager.keyArrowPressed.emit()
	# 		print('a')
	#
	# 	target.keyPressEvent = types.MethodType(keyPressEvent, target)




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


