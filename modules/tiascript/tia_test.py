import ESVision
import logging

logging.basicConfig(level=logging.INFO)

#ESVision.Hardware(4)
esv = ESVision.Application()
esv.AcquisitionManager.SetAnnotationDisplay('Scanning Search', 'Search BF Scanning Display1')

esv.AcquisitionManager.SetAcquireAnnnotation((-800e-9,5e-6, 0, 0))

logging.info(esv.AcquisitionManager.SignalNames())

name = ESVision.Signals(esv.AcquisitionManager.SignalType('EDX')).name
name
ESVision.Signals[name]
