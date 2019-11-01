import logging
import os
path = os.path.dirname(os.path.abspath(__file__))

import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5.QtWidgets import QTreeView, QTableView
import PyQt5.QtWidgets as Widgets

from PyQt5.QtCore import QAbstractItemModel
import PyQt5.QtCore as Core
import PyQt5.QtGui as Gui

from useTEM_ui import UseTEMUI


import useTEM.pluginManagement as plugm
import logging
import os
path = os.path.dirname(os.path.abspath(__file__))

import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow

from useTEM_ui import UseTEMUI
from PyQt5.Qt import QFile
from PyQt5 import uic

class TreeWidget(Widgets.QTreeWidget):

	def dropEvent(self, event):

		dragItem = self.currentItem()
		Widgets.QTreeWidget.dropEvent(self, event)

		# pos = event.pos()
		#
		# item = self.itemAt(pos)

		#
		# if item:
		# 	ind = self.indexOfTopLevelItem(dragItem)
		# 	temp = self.takeTopLevelItem(ind)
		#
		# 	index = self.indexOfTopLevelItem(item)
		#
		# 	self.insertTopLevelItem(index, temp)
		# 	dragItem = temp

		# 	oldDragItemData = dragItem.data
		#
		# 	item.data = oldDragItemData
		# 	dragItem.data = oldItemData

		# if item:
		#
		# 	index = self.indexFromItem(item)
		# 	self.move(index,dragItem)
			# self.model().setData(index, 0, Core.Qt.UserRole)

		# if item is self.currentItem():
		# 	Widgets.QTreeWidget.dropEvent(self, event)
		# 	event.accept()
		# 	return

		data = dragItem.data
		lineEdit = Widgets.QLineEdit()
		lineEdit.setText(str(data['stuff']))
		# lineEdit.setFixedWidth(50)

		self.setItemWidget(dragItem, 0, lineEdit)

		# self.updateGeometry()


#
if __name__ == '__main__':


	app = QApplication(sys.argv)

	treeview = TreeWidget()

	treeview.setDragDropMode(Widgets.QAbstractItemView.InternalMove)
	# plugsTree.setSelectionMode(QtCore.Qt.QAbstractItemView::ExtendedSelection);
	treeview.setDragEnabled(True)
	treeview.setAcceptDrops(True)
	treeview.setDropIndicatorShown(True)

	item = Widgets.QTreeWidgetItem()
	item.data = {'stuff':1}
	lineEdit = Widgets.QLineEdit()
	lineEdit.setText(str(item.data['stuff']))
	# lineEdit.editingFinished.connect()

	treeview.addTopLevelItem(item)
	treeview.setItemWidget(item,0,lineEdit)

	item = Widgets.QTreeWidgetItem()
	item.data = {'stuff':2}
	lineEdit = Widgets.QLineEdit()
	lineEdit.setText(str(item.data['stuff']))
	# lineEdit.editingFinished.connect()

	treeview.addTopLevelItem(item)
	treeview.setItemWidget(item,0,lineEdit)


	item = Widgets.QTreeWidgetItem()
	item.data = {'stuff':3}
	lineEdit = Widgets.QLineEdit()
	lineEdit.setText(str(item.data['stuff']))
	# lineEdit.editingFinished.connect()

	treeview.addTopLevelItem(item)
	treeview.setItemWidget(item,0,lineEdit)




	# treeview.setIndexWidget(model.index(1, 0, Core.QModelIndex()), Widgets.QSpinBox())

#
#     treeview.setItemDelegateForRow(1,delegate)
#
	treeview.show()
#
	sys.exit(app.exec_())
#
#
