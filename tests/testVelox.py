import matplotlib.pyplot as plt
import numpy as np
from pywinauto import mouse,keyboard
from pywinauto.application import Application
from time import sleep
import re
import useTem.constants

import useVelox
#%%
# for automatic start of the software
#app = Application(backend="uia").start("C:\Program Files\Thermo Scientific Velox\Velox.exe")

# for connecting the started software


#app.AcquisitionVelox.print_control_identifiers()



#%% For doing STEM imaging
class veloxauto:

    titlebar=[]
    menu=[]

    def connectToServer(self):

        self.veloxConnect = app(backend="uia").connect(path=r"C:\Program Files\Thermo Scientific Velox\Velox.exe")
        self.vtoolbar = self.veloxConnect.top_window().Toolbar
        self.vstatusbar = self.veloxConnect.top_window().Statusbar




#%%
#check status
app = Application(backend="uia").connect(path=veloxPath)
tool_bar = app.top_window().Toolbar
status_bar = app.top_window().StatusBar
# optics
stem = tool_bar.STEM
tem = tool_bar.TEM

#detectors
haadf = tool_bar.HAADF
df4 = tool_bar.DF4
df2 = tool_bar.DF2
bf = tool_bar.BF

#stem_imaging tab controls
beam_blank = tool_bar.Custom10.checkBox0
focus_box = tool_bar.Custom10.checkBox2
search = tool_bar.Custom10.checkBox3
acquire = tool_bar.Custom10.checkBox4
preview = tool_bar.Custom10.checkBox5
video = tool_bar.Custom10.checkBox6


#%%


while(True):
    status = status_bar.Static.window_text()
    pattern = r'\b(?:Acquisition|complete)\b'
    m = re.findall(pattern,status)

    if len(m)== 2:
        break


#%%


app.top_window().ComboBox2.type_keys("%{DOWN}")
app.top_window().ComboBox2.descendants()
child_window(ListBox.children()
#print_control_identifiers()
#select('14 mm')#child_window(best_match='ListBox').print_control_identifiers()
#child_window(0).print_control_identifiers()


(title="4.5 m").select('4.5 m')

mag_neg = app.top_window().Button6
mag_pos = app.top_window().Button7

cl_neg= app.top_window().Button4
cl_pos= app.top_window().Button5

app.top_window().Button4.click()
#ListBox.print_control_identifiers()



if stem_tab.get_toggle_state()==0:
    tool_bar.STEM.click_input()

if haadf_tab.get_toggle_state()==0:
    tool_bar.HAADF.click_input()




if beam_blank.get_toggle_state()==1:
    beam_blank.click_input()

tool_bar.Custom10.checkBox6.click_input()

tool_bar.Custom10.print_control_identifiers()
#%%
tool_bar.STEMImaging.print_control_identifiers()








#tem_stat = app.top_window().Toolbar.TEM.get_toggle_state()



#print(app.top_window().Toolbar.STEM.get_toggle_state())
#app.top_window().Toolbar.TEM.click_input()

#app.top_window().menu2.Optics.select()
#app.top_window().STEM.select()
#app.top_window().STEM.click()

#%%

#app.top_window().Toolbar.HAADF.click_input()
app.top_window().HAADFmrad.get_properties()




#%% click on HAADF
app.top_window().Toolbar.HAADF.toggle()
app.top_window().Toolbar.HAADF.get_toggle_state()









#%%
app_menu = app.top_window().descendants(control_type="MenuBar")
app_menu.children()


app.ProcessingVelox.Menu.print_control_identifiers()
app.print_control_identifiers()#['menu bar']['File Alt+F']#.get_items()#['Open... Ctrl+O']
#%%
#app = Application(backend="win32").connect(handle=0x540D12)

dialogs = app.windows()
#print(dialogs)

app['Beam Settings']['TEM'].click()

# scrollbar click 0 (up) 1 (down)
app.Stigmator.Stigmator_main.ScrollBar1.click()

app.Stigmator.Stigmator_main.Diffraction.click()
#app.Stigmator.Stigmator_main.print_control_identifiers()

#app.Stigmator.Objective.click()

app.Stigmator.Spin1UpDown.increment()
app.Workset.Tab1.select(2)

#print(dialogs)
#main_window = dialogs[0]

#print(main_window.children()[0].children()[0].)

#workset.children()[0].select()







#b = dialogs[0].children()
#c = b[0].descendants()





a = np.zeros((5,5), np.uint8, 0)
