import autoSTEM
import numpy as np
import re
import PIL
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
from skimage import feature,filters
from scipy import stats
#%%

stem=autoSTEM.autoSTEM()
stem.connectToServer()




for i in range(0,50):

    p = stem.flucamConnect.FluCamViewer.pane.capture_as_image()
    plt.imshow(p)
    plt.show()


stem.screen('in')


### auto tune the microscope
stem.colval('open')
stem.mode('STEM')
stem.detector({'HAADF'})
stem.img_mode('search')
## go to an area of interest
stem.search_off()
stem.screen('in')

stem.colval('close')

stem.scan_rotation(0,'abs')
stem.focus_box('off')
stem.defocus(10,'current')
stem.manual_video(5)
stem.revstem(10,90)
