from comtypes.client import CreateObject, Constants
from comtypes.gen import ESVision

from comtypes.gen import TEMScripting
from comtypes.gen import TecnaiPortal
from comtypes.server.register import UseCommandLine

from comtypes.client import GetModule

testlib = GetModule("C:\\Program Files (x86)\\FEI\\TIA\\Bin\\ESVision.tlb")
from comtypes.gen.ESVision import Position2D
import comtypes.gen.ShDocVw
import comtypes
import comtypes.server.localserver

script.Move()
script.X

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

aqm = engine.AcquisitionManager()

enum = aqm.SignalNames
enum.item(0)

posCollection = ESVision.IPositionCollection()
positions = ((0,1), (9,2))
for pos in positions:
    esPos = CreateObject(ESVision)

    posCollection.AddPosition(posCollection,0,1)

for i in enumerate(enum):
    print(i)
engine.ScanningServer().FrameWidth = 500;
engine.ScanningServer().FrameHeight= 500;
engine.ScanningServer().DwellTime = 40e-6;


engine.AcquisitionManager().SelectSetup("View Image");


acq = engine.AcquisitionManager().Start()
acq

engine.GetRowCount(3)
engine.Exit()
