import microscope
import matplotlib.pyplot as plt
import numpy as np

A= microscope.Microscope()


A.get_vacuum()
column_valves_open()
# scan rotation (measured in radians)
A.get_stem_rotation()*180/np.pi
A.set_stem_rotation(np.pi/4)

# defous is in meters
A.get_defocus()

for i in range(-400,500,10):
    A.set_defocus(0.000000001*i)
A.get_defocus()

# setting stage position
set_s = A.get_stage_position()
#pos_A=  [('a',0.01),('b',0.01),('x',0.00005),('y',0.00002),('z',0.00005),('method', "MOVE")]
A.set_stage_position(pos_A)

# DiffractionShift
A.get_diffraction_shift()
A.set_diffraction_shift((0.08,0.8))

# Condenser Stigmator (value -1 to 1)
A.get_condenser_stig()
A.set_condenser_stig((0,0))

# beam blanker
A.set_beam_blanked(0)
A.get_beam_blanked()


#Detector
A.get_detectors()
p = A.get_detector_param("BF")
p

p['binning'] = 4
p['dwelltime(s)'] = 0.4e-6
A.set_detector_param("BF", p)
A.set_image_shift((0,0))
g = A.acquire("BF")
g
plt.imshow(g)

A.get_voltage()
print(t)
