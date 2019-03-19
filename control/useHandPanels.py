import pywinauto as win

from pywinauto.application import Application as app
from pywinauto import keyboard  as keys

class UseHandPanels:

    handpanels = None

    coords = {
        'mf_x': (333,109),
        'mf_y': (445,109),
        'int': (218,109),
        'a_tilt': (57,83),
        'b_tilt': (46,127),
        'int_fine': (206,77),
        'int_coarse': (230,77),
        'exposure': (274,82),
        'mf_fine': (314,79),
        'mf_coarse': (337,79),
        'L1': (357,168),
        'L2': (359,195),
        'L3': (361,219),
        'R1': (421,168),
        'R2': (416,195),
        'R3': (413,219),
        'mag': (505,109),
        'diffraction': (509,81),
        'dark_field': (453,79),
        'wobbler': (551,80),
        'focus': (565,130),
        'focus_step': (0,0),
        'z': (744,125),
        'stigmator': (273,121)
    }

    controls = dict()

    def __init__(self, pathToExe):

        try:
            connectedApp = app(backend='uia').connect(path=pathToExe)
        except win.application.ProcessNotFoundError:
            connectedApp = app(backend='uia').start(pathToExe)

        self.handpanels = connectedApp.top_window()
        self._pulses_offset = 22

        controls = self.handpanels.descendants()

        for control in controls:

            # test if the control is the pane
            if type(control) is win.controls.uiawrapper.UIAWrapper:
                paneRect = control.rectangle()
                paneRect.top -= 20


			# # test if the control is an edit wrapper

            elif type(control) is win.controls.uia_controls.EditWrapper:

                controlRect = control.rectangle()
                controlRect.left = controlRect.left-paneRect.left
                controlRect.right = controlRect.right-paneRect.left
                controlRect.top = controlRect.top-paneRect.top
                controlRect.bottom = controlRect.bottom-paneRect.top

                for label in self.coords:
                    pos = self.coords[label]

                    newPos = (pos[0], pos[1]+self._pulses_offset)

                    if self.rect_contains(controlRect,newPos):
                        self.controls[label] = control


    def rect_contains(self,rect, point):


    	if rect.left > point[0]:
    		return False
    	elif rect.right < point[0]:
    		return False
    	elif rect.top > point[1]:
    		return False
    	elif rect.bottom < point[1]:
    		return False

    	return True

    def _click(self, position, steps):

        for _ in range(steps):
            self.handpanels.click_input(coords=position, absolute=False)

    def _double_click(self, position):

        self.handpanels.click_input(coords=position, absolute=False, double=True)


    # Magnficication

    def magnification(self, steps):

        pos = self.coords['mag']
        self._click(pos, steps)


    def set_mag_pulses(self, steps):
        self.controls['mag'].set_text(str(steps))

    def get_mag_pulses(self, steps):
        return self.controls['mag'].get_value()


    # Multifunction knobs
    def mf_x(self, steps):

        pos = self.coords['mf_x']
        self._click(pos, steps)

    def mf_y(self, steps):

        pos = self.coords['mf_y']
        self._click(pos, steps)

    def set_mf_pulses(self, steps):
        self.controls['mf_y'].set_text(str(steps))
        self.controls['mf_x'].set_text(str(steps))

    def get_mf_pulses(self, steps):

        x = self.controls['mf_x'].get_value()
        y = self.controls['mf_y'].get_value()

        return (x, y)

    # Focus knobs

    def focus(self, steps):

        pos = self.coords['focus']
        self._click(pos, steps)

    def set_focus_pulses(self, steps):
        self.controls['focus'].set_text(str(steps))

    def get_focus_pulses(self, steps):
        return self.controls['focus'].get_value()


    def focus_step(self, steps):

        pos = self.coords['focus_step']
        self._click(pos, steps)

    def set_focus_step_pulses(self, steps):
        self.controls['focus_step'].set_text(str(steps))

    def get_focus_step_pulses(self):
        return self.controls['focus_step'].get_value()

    # Intensity knobs

    def intensity(self, steps):

        pos = self.coords['int']
        self._click(pos, steps)

    def set_int_pulses(self, steps):
        self.controls['int'].set_text(str(steps))
    # Sample tilt

    def a_tilt(self, steps):

        pos = self.coords['a_tilt']
        self._click(pos, steps)

    def set_a_tilt_pulses(self, steps):
        self.controls['a_tilt'].set_text(str(steps))

    def get_a_tilt_pulses(self):
        return self.controls['a_tilt'].get_value()

    def b_tilt(self, steps):
        pos = self.coords['b_tilt']
        self._click(pos, steps)

    def set_b_tilt_pulses(self, steps):
        self.controls['b_tilt'].set_text(str(steps))

    def get_b_tilt_pulses(self):
        return self.controls['b_tilt'].get_value()


    # Stage controls

    def z(self, steps):
        pos = self.coords['z']
        self._click(pos, steps)

    def set_z_pulses(self, steps):
        self.controls['z'].set_text(str(steps))


    def get_z_pulses(self, steps):
        return self.controls['z'].get_value()

    # Other buttons


    def stigmator(self):
        pos = self.coords['stigmator']
        self._click(pos, 1)

    def diffraction(self):
        pos = self.coords['diffraction']
        self._click(pos, 1)

    def wobbler(self):
        pos = self.coords['wobbler']
        self._click(pos, 1)

    def dark_field(self):
        pos = self.coords['dark_field']
        self._click(pos, 1)

    def int_fine(self, steps):
        pos = self.coords['int_fine']
        self._click(pos, steps)

    def int_coarse(self, steps):
        pos = self.coords['int_coarse']
        self._click(pos, steps)

    def exposure(self):
        pos = self.coords['exposure']
        self._click(pos, 1)

    def mf_coarse(self, steps):
        pos = self.coords['mf_coarse']
        self._click(pos, steps)

    def mf_fine(self, steps):
        pos = self.coords['mf_coarse']
        self._click(pos, steps)

    def R(self, buttonNum):
        pos = self.coords['R'+str(buttonNum)]
        self._click(pos, 1)


    def L(self, buttonNum):
        pos = self.coords['L'+str(buttonNum)]
        self._click(pos, 1)
