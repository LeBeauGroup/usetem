
from PyQt5 import QtCore
from .workflowtreewidget import WorkflowItem
import re

class WorkflowThread(QtCore.QThread):

	currentWorkflowItemDidChange = QtCore.pyqtSignal(WorkflowItem)
	workflowFinished = QtCore.pyqtSignal()
	workflowItemNeedsUpdate = QtCore.pyqtSignal(WorkflowItem)
	workflowConditionalFailed = QtCore.pyqtSignal(str, str)


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

	def processIfStatement(self, statement):

		# match all variable names and replace with params[varName]
		insertedParams = re.sub('(?!and|or|not|is|in|True|False)(?![\'\"])(\\b[a-zA-Z_][a-zA-Z0-9]+\\b)(?![\'\"])',
		                        'params[\'\\1\']',
		                        statement)

		return insertedParams

	def run(self):

		def execute(runItem, lastResult):

			params.update(runItem.data)
			itemData = runItem.data
			pluginName = itemData['name']

			if pluginName in ['elseIf']:
				print('it is an elseIf')
				pluginName = 'conditional'

			plugin = self.plugins[pluginName]
			plugin.setInterfaces(self.interfaces)
			newResult = None

			if runItem.childCount() > 0:

				if itemData['name'] == 'conditional':

					for condIndex, condition in enumerate(itemData['conditions']):
						testCriterion = condition
						testString = self.processIfStatement(testCriterion)

						if testString == '':
							continue
						evalResult = None

						try:
							print(params)
							evalResult = eval(testString)
						except Exception as e:
							self.workflowConditionalFailed.emit('Conditional Failed', 'Invalid if statement: '+ testString)
							self.exit(False)

						if evalResult:

							conditionChild = runItem.child(condIndex)
							print(condIndex)

							for ind in range(conditionChild.childCount()):

								childToRun = conditionChild.child(ind)
								execute(childToRun, lastResult)

							break

				elif pluginName in ['forLoop', 'forList']:

					loopParameters = runItem.data
					loopValues = plugin.run(loopParameters)
					print(loopValues)
					for value in loopValues:
						for ind in range(runItem.childCount()):
							childToRun = runItem.child(ind)

							if not loopParameters['variableName'] == 'None':
								variableName = loopParameters['variableName']

								if variableName in list(childToRun.data.keys()):

									childToRun.data.update({variableName:value})
									self.workflowItemNeedsUpdate.emit(childToRun)

							self.currentWorkflowItemDidChange.emit(childToRun)
							execute(childToRun, lastResult)
			else:


				try:
					newResult = plugin.run(params, result=lastResult)
				except Exception as e:
					print(e)
					self.exit()

			print(params)
			return newResult

		result = None
		params = {}


		for itemIndex in range(self.workflow.topLevelItemCount()):

			topLevelItem = self.workflow.topLevelItem(itemIndex)

			itemToRun = topLevelItem
			self.currentWorkflowItemDidChange.emit(itemToRun)
			# parameters.update(itemToRun.data)
			result = execute(itemToRun, result)

		self.workflowFinished.emit()