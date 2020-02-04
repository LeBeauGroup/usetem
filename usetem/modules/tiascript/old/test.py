from comtypes.client import CreateObject, Constants
from comtypes.gen import ESVision
from comtypes.gen import TEMScripting
from comtypes.gen import TecnaiPortal

v = ESVision.IVector()

acq2 = ESVision.AcquisitionManager()
v.X = 5

script = CreateObject('FeiTadHandPanels.TadHandPanelsBrick.1')
script.value

val = 0
script.TemperatureControl.RefrigerantLevel(val)

script = CreateObject("peouicStemAutoTuning.StemAutoTuningClusterControl")

script.

script.IPiaControl.GetDeviceCount()
pos =script.Stage.Position
pos.X

b = Constants(script)
b
b.hoSingleTilt
script.Stage.Goto(pos, TEMScripting.StageAxes )
v.X

)
engine = CreateObject("ESVision.Application")

acq = engine.AcquisitionManager().acquire()
acq

engine.GetRowCount(3)
engine.Exit()
