import esvision
import logging
import pickle

logging.basicConfig(level=logging.INFO)

#ESVision.Hardware(4)
esv = esvision.Application()
#esv.AcquisitionManager.SetAnnotationDisplay('Scanning Search', 'Search BF Scanning Display1')
#esv.AcquisitionManager.SetAcquireAnnnotation((-800e-9,5e-6, 0, 0))

#logging.info(esv.AcquisitionManager.SignalNames())
bc = esv.BeamControl

window = pickle.loads(esv.ActiveDisplayWindow().data)

print(window)

ss = esv.ScanningServer
names = ss.MagnificationNames('Imaging')


ss.ReferencePosition((0,1))
print(ss.MagnificationName(1, 'Imaging'))

ss.CreateMagnification(800, (0, 0, 1, 1),  'Imaging')

ss.DeleteMagnification('800 X',  'Imaging')

bc.PositionCalibrated(False)
#bc.SetLineScan((-1,0),(0,1), 100)

bc.SetFrameScan((0.0,0.0, 1.0,1.0), 100, 100)


bc.SetContinuousScan()
bc.DwellTime(1e-5)
bc.Start()

#bc.Stop()
