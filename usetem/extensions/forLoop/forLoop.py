import usetem.pluginTypes as pluginTypes
import numpy as np



class ForLoop(pluginTypes.IExtensionPlugin):

    def __init__(self):

        super(ForLoop, self).__init__()
        self.defaultParameters.update({'start': '1', 'step': '1', 'stop': '10', 'variableName': 'None'})
        self.acceptsChildren = True



    def run(self, params=None, result=None):

        print('trying to run ')
        start = float(params['start'])
        step = float(params['step'])
        stop = float(params['stop'])

        values = np.arange(start, stop, step)
        listOfValues = values.tolist()

        listOfValues.append(stop)

        return  listOfValues
