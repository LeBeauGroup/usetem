from useTEM.pluginTypes import ITechniquePlugin
import abc

class ISTEMImage(ITechniquePlugin):

	client = None

	def acquire(self):
		print('acquiring')
