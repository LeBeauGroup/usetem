# -*- coding: utf-8 -*-
"""

"""

from pywinauto import Application as app
from pywinauto import keyboard
from constants import *

class PanelSelector:

	def __init__(self,selector):
		self.selector = selector

	def select(self, title):

		self.selector.click()
		self.selector.select(title)

	def print_items(self):
		print(self.selector.texts())

	def available_panels(self):
		return self.selector.texts()



class UseTemInterface:

    temserver = []

    Vacuum = []
    STEMImaging = []
    STEMDetectors = []
    Stigmators = []
    Workset = []
    Stage2 = []
    PanelSelector = []

    available_panels = []
    tab_panels = []


    def __init__(self):
        self.temserver = app(backend="win32").connect(path=peouiPath)
        self.Workset = self.temserver.Workset.Tab1
        self.Stage2 = self.temserver['Stage²']
        self.Vacuum = self.temserver.VacuumSupervisor
        #self.temserver.InfoArea.IDB_OPTIONCLUSTER_FRAMESWITCH_TASKBAR_SF.click()
        #self.temserver.InfoArea.IDB_BTN_APPSELECT_SF.click()

        # click to open the tools flap
        #self.temserver.InfoArea.ComboBox2.click()
        print(self.Workset.texts())
        self.PanelSelector = PanelSelector(self.temserver.InfoArea.ComboBox2)

        self.learn_interface()

        #IDB_BTN_NONE_OPTIONCLUSTER_SF

    def learn_interface(self):

    	#self.temserver.DarkField.parent()
    	#print(self.temserver.windows())

    	selected = self.Workset.get_selected_tab()
    	available_panels = []
    	tab_panels = dict()

    	for i in range(0, self.Workset.tab_count()):
    		self.Workset.select(i)
    		tab_name = self.Workset.get_tab_text(i)
    		p = self.PanelSelector.available_panels()
    		available_panels += p

    		tab_panels[tab_name] = p
    		keyboard.SendKeys('{VK_ESCAPE}')

    	# set class varaible for available panels

    	self.available_panels = set(available_panels)


    	for tab in tab_panels:
    		tab_panels[tab] = list(self.available_panels.difference(set(tab_panels[tab])))

    	self.tab_panels = tab_panels

    	self.Workset.select(selected)

    def make_control_available(self, control):

    	# determine selected tab
    	selected = self.Workset.get_selected_tab()
    	tab_name = self.Workset.get_tab_text(selected)

    	if control in self.tab_panels[tab_name]:
    		pass
    	else:
    		self.PanelSelector.select(control)



#%%


#
# tem = TEMauto()
# tem.connectToServer()
# tem.make_control_available('STEM Imaging (Expert)')
# tem.temserver['STEM Imaging (Expert)'].STEM.click()
#tem.PanelSelector.select('Normalizations')
#tem.Vacuum['Col. Valves Closed'].click()
