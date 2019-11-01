import PyQt5.QtWidgets as Widgets
import PyQt5.QtCore as Core

class WorkflowTreeWidget(Widgets.QTreeWidget):

	# def __init__(self):
	#
	# 	# super.__init__()
	# 	self.setDragDropMode(Widgets.QAbstractItemView.InternalMove)
	# 	# plugsTree.setSelectionMode(QtCore.Qt.QAbstractItemView::ExtendedSelection);
	# 	self.setDragEnabled(True)
	# 	self.setAcceptDrops(True)
	# 	self.setDropIndicatorShown(True)

	def dropEvent(self, event):

		dragItem = self.currentItem()

		print(self.indexFromItem(dragItem).row())
		Widgets.QTreeWidget.dropEvent(self, event)

		for i in range(0, self.topLevelItemCount()):
			item =self.topLevelItem(i)
			name = item.data['name']

			uiWidget = self.plugins[name].ui(item)

			self.setItemWidget(item, 0, uiWidget)

			# self.viewport().update()
		# self.updateGeometry()

