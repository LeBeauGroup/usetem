import yapsy.IPlugin as plugin
import os, sys
from PyQt5 import QtCore, QtWidgets, uic, QtGui
from yapsy.PluginManager import PluginManager
import bibtexparser

class ITechniquePlugin(plugin.IPlugin):
	pass

class IExtensionPlugin(plugin.IPlugin):

	def __init__(self):
		super(IExtensionPlugin, self).__init__()

		filePath = sys.modules[self.__module__].__file__.split(os.extsep)[0]
		name = os.path.basename(filePath)

		uiPath = filePath + '.ui'

		self.uiFile = QtCore.QFile(uiPath)
		self.uiFile.open(QtCore.QFile.ReadOnly)

		self.defaultParameters = {'name':name, 'displayName':''}
		self.acceptsChildren = False
		self.parameterTypes = {}

	def ui(self, item, parent=None):

		def updateItemData():

			sender = widget.sender()
			senderName = sender.objectName()

			if "Edit" in senderName:
				key = senderName.replace('Edit', '')

				if isinstance(sender, QtWidgets.QLineEdit):
					text = sender.text()

					if isinstance(sender.validator(), QtGui.QIntValidator):
						value = int(text)
					elif isinstance(sender.validator(), QtGui.QDoubleValidator):
						value = float(text)
					else:
						value = text

					widget.item.data[key] = value

				elif isinstance(sender, QtWidgets.QListWidget):
					newSelection = list()

					for selectedItem in sender.selectedItems():
						text = selectedItem.text()
						newSelection.append(text)

					widget.item.data[key] = newSelection

				elif isinstance(sender, QtWidgets.QComboBox):
					widget.item.data[key] = sender.currentText()

			if "Add" in senderName:
				key = senderName.replace('Add', '')

				if isinstance(sender, QtWidgets.QLineEdit):
					text = sender.text()

					theItem = widget.item
					currentList = theItem.data[key]
					currentList.append(text)

					tree = theItem.treeWidget()

					widget.item.data[key] = currentList
					tree.setItemWidget(theItem,0, self.ui(theItem))

		# Make sure we are at the start of the file and then load

		self.uiFile.seek(0)

		topWidget = QtWidgets.QWidget()
		layout = QtWidgets.QVBoxLayout()

		hline = QtWidgets.QFrame()

		hline.setFrameShape(QtWidgets.QFrame.HLine)


		label = QtWidgets.QLabel(item.data['displayName'])
		font = QtGui.QFont()
		font.setPointSize(7)
		font.setBold(True)
		label.setFont(font)
		label.setFixedHeight(20)
		layout.addWidget(label)
		layout.setObjectName('layout')
		layout.addWidget(hline)

		widget: QtWidgets = uic.loadUi(self.uiFile)
		widget.item = item
		widget.setObjectName('widget')

		layout.addWidget(widget)


		for child in widget.findChildren(QtWidgets.QWidget):

			name = child.objectName()

			if "Edit" in name:

				parameterName = name.replace('Edit', '')

				if isinstance(child, QtWidgets.QListWidget):

					for it in range(0, child.count()):

						rowItem = child.item(it)
						label = rowItem.text()

						print(item.data[parameterName])

						if label in item.data[parameterName]:
							rowItem.setSelected(True)
						else:
							rowItem.setSelected(False)

					child.itemSelectionChanged.connect(updateItemData)

				elif isinstance(child, QtWidgets.QLineEdit):
					child.setText(f'{item.data[parameterName]}')
					child.editingFinished.connect(updateItemData)

					try:
						if self.parameterTypes[parameterName] is int:
							child.setValidator(QtGui.QIntValidator())
						if self.parameterTypes[parameterName] is float:
							child.setValidator(QtGui.QDoubleValidator())
					except Exception as e:
						print('validator could not be set')

				elif isinstance(child, QtWidgets.QComboBox):
					paramValue = item.data[parameterName]
					for ind in range(0, child.count()):

						if child.itemText(ind) == str(paramValue):
							child.setCurrentIndex(ind)
							break
					child.currentIndexChanged.connect(updateItemData)

			if "Add" in name:
				key = name.replace('Add', '')

				if isinstance(child, QtWidgets.QLineEdit):
					child.editingFinished.connect(updateItemData)


			if "View" in name:

				parameterName = name.replace('View', '')
				if isinstance(child, QtWidgets.QListWidget):

					for label in item.data[parameterName]:

						child.addItem(QtWidgets.QListWidgetItem(label))

		widgetSize:QtCore.QSize = widget.size()

		topWidget.setFixedHeight(widgetSize.height()+60)
		topWidget.setLayout(layout)

		item.setSizeHint(0, topWidget.size())


		return topWidget

	def setInterfaces(self, interfaces):
		self.interfaces = interfaces

	def citations(self):
		filePath = sys.modules[self.__module__].__file__.split(os.extsep)[0]
		bibPath = filePath + '.bib'

		try:
			with open(bibPath) as bibfile:
				pluginBib = bibtexparser.load(bibfile)
		except Exception:
			pluginBib = None


		return pluginBib






# categories = {'Control' : IInterfacePlugin,
#    		'Technique' : ITechniquePlugin, 'Extension':IExtensionPlugin}

class IInterfacePlugin(plugin.IPlugin):

	def loadTechniques(self,techniquesPath, controls=None):


		# Build the manager, set load location, and then collect them

		pm = PluginManager()
		pm.updatePluginPlaces([techniquesPath])
		pm.collectPlugins()

		self.techniques = dict()

		for pluginInfo in pm.getAllPlugins():
			print('loading '+ pluginInfo.name + ' for: ' + self.name)
			# Get the object and store in dictionary

			self.techniques[pluginInfo.name] = pluginInfo.plugin_object
			self.techniques[pluginInfo.name].controlPlugins = controls


class IWorkflow(plugin.IPlugin):
	pass
