import PyQt5.QtWidgets as Widgets
import PyQt5.QtCore as Core

class WorkflowItem(Widgets.QTreeWidgetItem):
	pass




class WorkflowTreeWidget(Widgets.QTreeWidget):

	def __init__(self, parent):
		super().__init__(parent)
	#
		# self.setStyleSheet("QTreeWidget::item {border: 1px solid black; margin-top: 2px}")

	# def __init__(self):
	#
	# 	# super.__init__()
	# 	self.setDragDropMode(Widgets.QAbstractItemView.InternalMove)
	# 	# plugsTree.setSelectionMode(QtCore.Qt.QAbstractItemView::ExtendedSelection);
	# 	self.setDragEnabled(True)
	# 	self.setAcceptDrops(True)
	# 	self.setDropIndicatorShown(True)

	def keyPressEvent(self, event):
		currentItem = self.currentItem()

		pluginName = currentItem.data['name']

		if pluginName in ['elseIf', 'else']:
			super(WorkflowTreeWidget, self).keyPressEvent(event)
			return

		print(f'sending {pluginName} an event')

		try:

			plugin = self.plugins[pluginName]
			if plugin.isRunning:
				plugin.updateEvent(event)
			else:
				super(WorkflowTreeWidget, self).keyPressEvent(event)

		except AttributeError:
			super(WorkflowTreeWidget, self).keyPressEvent(event)

		#selectedItem.event = event



	def resetItem(self, theItem):
		name = theItem.data['name']

		if name in ['elseIf', 'else']:
			uiWidget = self.plugins['conditional'].ui(theItem)
			self.setItemWidget(theItem, 0, uiWidget)

		else:
			uiWidget = self.plugins[name].ui(theItem)
			self.setItemWidget(theItem, 0, uiWidget)

		if theItem.childCount() > 0:

			for childIndex in range(0, theItem.childCount()):
				self.resetItem(theItem.child(childIndex))

	def dropEvent(self, event):

		dragItem = self.currentItem()

		if dragItem.data['name'] is 'elseIf':
			return

		Widgets.QTreeWidget.dropEvent(self, event)

		# Todo: update to handel children redraw

		for i in range(0, self.topLevelItemCount()):
			item =self.topLevelItem(i)
			self.resetItem(item)



			# self.viewport().update()
		# self.updateGeometry()

