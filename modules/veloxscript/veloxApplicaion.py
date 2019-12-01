import numpy as np
import re
import PIL
import matplotlib.pyplot as plt
import microscope

from pywinauto import mouse,keyboard
from pywinauto.application import Application as app


class Application():

    veloxConnect = []

    vtoolbar = []
    vstatusbar=[]


    def connectToServer(self):

        self.veloxConnect = app(backend="uia").connect(path=r"C:\Program Files\Thermo Scientific Velox\Velox.exe")
        self.vtoolbar = self.veloxConnect.top_window().toolbar
        self.vstatusbar = self.veloxConnect.top_window().statusbar


    def changeMode(self,value):
        temMode = self.vtoolbar.TEM.get_toggle_state()
        stemMode = self.vtoolbar.STEM.get_toggle_state()
        if temMode==0 and stemMode==1:
            currMode='STEM'
        elif temMode==1 and stemMode==0:
            currMode='TEM'
        if currMode=='TEM' and value=='STEM':
            self.vtoolbar.STEM.click_input()
        elif currMode=='STEM' and value=='TEM':
            self.vtoolbar.TEM.click_input()


    def selectDetector(self,value):
        allDetect = {'HAADF','BF','DF4','DF2'}

        diff = allDetect-value
        for ind in diff:
            indState = self.vtoolbar.child_window(best_match=ind).get_toggle_state()
            if indState==1:
                self.vtoolbar.child_window(best_match=ind).click_input()

        for id in value:
            idState = self.vtoolbar.child_window(best_match=id).get_toggle_state()
            if idState==0:
                self.vtoolbar.child_window(best_match=id).click_input()

    def removeHaadf(self):
        indState = self.vtoolbar.child_window(best_match='HAADF').get_toggle_state()
        if indState==1:
            self.vtoolbar.child_window(best_match='HAADF').click_input()

    def focusBox(self,value):
        fb = self.vtoolbar.Custom10.checkBox2
        fbMode = fb.get_toggle_state()
        if fbMode==0 and value=='on':
            fb.click_input()
        elif fbMode==1 and value=='off':
            fb.click_input()

    def changeImgmode(self,value):
        if value=='search':
            sch = self.vtoolbar.Custom10.checkBox3
            schMode = sch.get_toggle_state()
            if schMode==0:
                sch.click_input()

        elif value=='preview':
            pr = self.vtoolbar.Custom10.checkBox4
            prMode = pr.get_toggle_state()
            if prMode==0:
                pr.click_input()

        elif value=='acquire':
            ac = self.vtoolbar.Custom10.checkBox5
            acMode = ac.get_toggle_state()
            if acMode==0:
                ac.click_input()

        elif value=='video':
            vo = vtoolbar.Custom10.checkBox6
            voMode = vo.get_toggle_state()
            if voMode==0:
                vo.click_input()

    def searchOff(self):
        sch = self.vtoolbar.Custom10.checkBox3
        pr = self.vtoolbar.Custom10.checkBox5
        schMode = sch.get_toggle_state()
        prMode = pr.get_toggle_state()
        if schMode==1:
            sch.click_input()
        if prMode==1:
            pr.click_input()




# ######################### Extra functions created in a class ################################
#     def revstem(self,frames,angle):
#         for i in range(0,frames):
#             rot = angle*i
#             self.scan_rotation(rot,'abs')
#             self.changeImgmode('acquire')
#             while(True):
#                 status = self.vstatusbar.Static.window_text()
#                 pattern = r'\b(?:Acquisition|complete)\b'
#                 m = re.findall(pattern,status)
#
#                 if len(m)== 2:
#                     break
