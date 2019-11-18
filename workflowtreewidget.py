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

		if dragItem.data['name'] is 'elseIf':
			return

		Widgets.QTreeWidget.dropEvent(self, event)

		# Todo: update to handel children redraw

		def resetItem(theItem):
			name = theItem.data['name']

			if name in ['if', 'elseIf', 'else']:
				parentConditional = theItem.parent()
				parentWidget = self.itemWidget(parentConditional,0)

				uiWidget = self.plugins['conditional'].ui(theItem)
				self.setItemWidget(theItem, 0, uiWidget)
				# parentWidget.addElseIf.click()

			else:
				uiWidget = self.plugins[name].ui(theItem)
				self.setItemWidget(theItem, 0, uiWidget)

			if theItem.childCount() > 0:

				for childIndex in range(0, theItem.childCount()):
					resetItem(theItem.child(childIndex))


		for i in range(0, self.topLevelItemCount()):
			item =self.topLevelItem(i)
			resetItem(item)



			# self.viewport().update()
		# self.updateGeometry()

