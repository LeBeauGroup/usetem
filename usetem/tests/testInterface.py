import matplotlib.pyplot as plt
import numpy

import control.useHandPanels as hp
from constants import *
import control.useTemInterface as temUI
import pandas
import pywinauto
from pywinauto import clipboard
import pytesseract
import pyautogui as pag
from PIL import Image,ImageEnhance, ImageFilter

import mss
import numpy as np

from pytesseract import Output
import cv2



tUI = temUI.UseTemInterface()

#tUI.temserver.WorkspaceLayout.print_control_identifiers()

# current layout


rect = tUI.temserver.WorkspaceLayout.AfxWnd120u.rectangle()
img = tUI.temserver.WorkspaceLayout.AfxWnd120u1.capture_as_image()
img
pytesseract.pytesseract.tesseract_cmd=tesseractPath

folderImage = Image.open('images/workspace_folder.png')
minusImage = Image.open('images/workspace_minus.png')
plusImage = Image.open('images/workspace_plus.png')
minusImage

for im in pag.locateAll(plusImage, img):
    print('plus!')

# open all
while(True):
    img = tUI.temserver.WorkspaceLayout.AfxWnd120u1.capture_as_image()
    try:
        locs = list(pag.locateAll(plusImage, img))
    except:
        break
    tUI.temserver.WorkspaceLayout.AfxWnd120u0.click_input(button='left', coords=(locs[0].left, locs[0].top))

# close all
while(True):
    img = tUI.temserver.WorkspaceLayout.AfxWnd120u1.capture_as_image()
    try:
        locs = list(pag.locateAll(minusImage, img))
    except:
        break
    tUI.temserver.WorkspaceLayout.AfxWnd120u0.click_input(button='left', coords=(locs[0].left, locs[0].top))




for im in pag.locateAll(minusImage, img):
    print('minus!')
    tUI.temserver.WorkspaceLayout.AfxWnd120u0.click_input(button='left', coords=(im.left, im.top))


for im in pag.locateAll(folderImage, img):
    with mss.mss() as sct:

        mon = {'top': rect.top+im.top, 'left': rect.left+im.left+20, 'width': 50, 'height': im.height}

        out = sct.grab(mon)
        test = Image.frombytes("RGB", out.size, out.bgra, "raw", "BGRX")

        oldSize = test.size
        newSize = (oldSize[0]*3, oldSize[1]*3)

        test = test.resize(newSize)
        test = test.filter(ImageFilter.MedianFilter())

        enhancer = ImageEnhance.Contrast(test)
        test = enhancer.enhance(2)
        test = test.convert('L')

        test.save('test'+str(im.top)+'.jpg')
        d = pytesseract.image_to_string(test)
        print(d)

plt.imshow(test)


    #tUI.temserver.WorkspaceLayout.AfxWnd120u0.click_input(button='right', coords=(im.left, im.top))



    #pywinauto.keyboard.SendKeys('e')
    #pywinauto.keyboard.SendKeys('^c')
    #print(clipboard.GetData())


#pytesseract.image_to_string(nee)
#tUI.temserver.WorkspaceLayout.AfxWnd120u.scroll('right', 'line')
#tUI.make_control_available('Workspace Layout')

#tUI.

import useTem

useTem.control

import numpy
