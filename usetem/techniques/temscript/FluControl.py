import usetem.pluginTypes as pluginTypes

class IFluControl(pluginTypes.ITechniquePlugin):

	client = None
	instrument = None

	def raiseScreen(self):
		print('raising')

		screen = self.client.camera
		screen.mainScreenPosition(2)

	def lowerScreen(self):
		screen = self.client.camera

		screen.mainScreenPosition(3)


	def screenCurrent(self):
		screen = self.client.camera

		return screen.screenCurrent()
