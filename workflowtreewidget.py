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

		# Todo: update to handel children redraw

		def resetItem(theItem):

			if theItem.childCount() > 0:

				for childIndex in range(0, theItem.childCount()):

					resetItem(theItem.child(childIndex))

			name = theItem.data['name']

			uiWidget = self.plugins[name].ui(theItem)

			self.setItemWidget(theItem, 0, uiWidget)

		for i in range(0, self.topLevelItemCount()):
			item =self.topLevelItem(i)

			resetItem(item)



			# self.viewport().update()
		# self.updateGeometry()

