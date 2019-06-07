import numpy as np
import temscript
import re
import PIL
#import matplotlib.pyplot
import temscript

#from pywinauto import mouse,keyboard
#from pywinauto.application import Application as app


class UseTem:
    temserver = []

    veloxConnect = []
    mp = []
    vtoolbar = []
    vstatusbar=[]

    scan_rotation_val=[]
    defocus_val=[]

    flucamConnect=[]
    ftoolbar=[]



    def connectToServer(self):
        self.temserver = app(backend="win32").connect(path=r"c:\\Tecnai\Exe\peoui.exe")
        self.mp = temscript.microscope.Microscope()

        self.veloxConnect = app(backend="uia").connect(path=r"C:\Program Files\Thermo Scientific Velox\Velox.exe")
        self.vtoolbar = self.veloxConnect.top_window().Toolbar
        self.vstatusbar = self.veloxConnect.top_window().Statusbar

        self.flucamConnect = app(backend="uia").connect(path=r"c:\\Tecnai\Exe\FluCamViewer.exe")
        self.ftoolbar = self.flucamConnect.FlucamViewer.toolstrip1

####################from tem scripting#####################
    def colval(self,value):
        colValOpen = self.mp.get_ColValOpen()

        if colValOpen==False and value=='open':
            self.mp.set_ColValOpen(True)
        elif colValOpen==True and value=='close':
            self.mp.set_ColValOpen(False)

    def scan_rotation(self,value,state):
        curr_val = self.mp.get_stem_rotation()*180/np.pi

        if state=='abs':
            self.mp.set_stem_rotation(value/180*np.pi)
        elif state=='current':
            self.mp.set_stem_rotation((value+curr_val)/180*np.pi)

        self.scan_rotation_val = self.mp.get_stem_rotation()*180/np.pi


    def defocus(self,value,state):
        curr_val = self.mp.get_defocus()*10**9
        if state=='abs':
            self.mp.set_defocus(value/10**9)
        elif state=='current':
            self.mp.set_defocus((curr_val+value)/10**9)

        self.defocus_val = self.mp.get_defocus()*10**9




###############from velox ui############################
    def mode(self,value):
        tem_mode = self.vtoolbar.TEM.get_toggle_state()
        stem_mode = self.vtoolbar.STEM.get_toggle_state()
        if tem_mode==0 and stem_mode==1:
            curr_mode='STEM'
        elif tem_mode==1 and stem_mode==0:
            curr_mode='TEM'
        if curr_mode=='TEM' and value=='STEM':
            self.vtoolbar.STEM.click_input()
        elif curr_mode=='STEM' and value=='TEM':
            self.vtoolbar.TEM.click_input()


    def detector(self,value):
        all_detect = {'HAADF','BF','DF4','DF2'}
        # if len(value)==0:
        #     for index in all_detect:
        #         index_state = self.vtoolbar.child_window(best_match=index).get_toggle_state()
        #         if index_state==1:
        #             self.vtoolbar.child_window(best_match=index).click_input()

        diff = all_detect-value
        for ind in diff:
            ind_state = self.vtoolbar.child_window(best_match=ind).get_toggle_state()
            if ind_state==1:
                self.vtoolbar.child_window(best_match=ind).click_input()

        for id in value:
            id_state = self.vtoolbar.child_window(best_match=id).get_toggle_state()
            if id_state==0:
                self.vtoolbar.child_window(best_match=id).click_input()


    def focus_box(self,value):
        fb = self.vtoolbar.Custom10.checkBox2
        fb_mode = fb.get_toggle_state()
        if fb_mode==0 and value=='on':
            fb.click_input()
        elif fb_mode==1 and value=='off':
            fb.click_input()

    def img_mode(self,value):
        if value=='search':
            sch = self.vtoolbar.Custom10.checkBox3
            sch_mode = sch.get_toggle_state()
            if sch_mode==0:
                sch.click_input()

        elif value=='preview':
            pr = self.vtoolbar.Custom10.checkBox5
            pr_mode = pr.get_toggle_state()
            if pr_mode==0:
                pr.click_input()

        elif value=='acquire':
            ac = self.vtoolbar.Custom10.checkBox4
            ac_mode = ac.get_toggle_state()
            if ac_mode==0:
                ac.click_input()

        elif value=='video':
            vo = vtoolbar.Custom10.checkBox6
            vo_mode = vo.get_toggle_state()
            if vo_mode==0:
                vo.click_input()

    def search_off(self):
        sch = self.vtoolbar.Custom10.checkBox3
        pr = self.vtoolbar.Custom10.checkBox5
        sch_mode = sch.get_toggle_state()
        pr_mode = pr.get_toggle_state()
        if sch_mode==1:
            sch.click_input()
        if pr_mode==1:
            pr.click_input()




######################### Extra functions created in a class ################################
    def revstem(self,frames,angle):
        for i in range(0,frames):
            rot = angle*i
            self.scan_rotation(rot,'abs')
            self.img_mode('acquire')
            while(True):
                status = self.vstatusbar.Static.window_text()
                pattern = r'\b(?:Acquisition|complete)\b'
                m = re.findall(pattern,status)

                if len(m)== 2:
                    break

#################  Flucam functions ###########################
    def screen(self,value):
        scr_mode = self.ftoolbar.InsertScreen
        print(scr_mode)
        #scr_state = scr_mode.state()

        if scr_state==True and value=='in':
            scr_mode.click_input()
        elif scr_state==True and value=='out':
            scr_mode.click_input()
