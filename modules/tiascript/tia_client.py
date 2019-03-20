import xmlrpc.client
from xmlrpc.client import MultiCall, Boolean
from ESVision import Hardware


#with xmlrpc.client.ServerProxy("http://localhost:8001/tia") as proxy:
#
#     #proxy.AcquisitionManager.DeleteSetup("View Image");
#     #proxy.AcquisitionManager.Acquire()
#     proxy.AcquisitionManager.AcquireSet(((0,1e-9),(0,100e-9)), 100e-6)
#
#     try:
#         proxy.AcquisitionManager.AddSetup('Acquire Image')
#     except:
#         pass
#
#     proxy.ScanningServer.FrameWidth(100)
#     proxy.ScanningServer.FrameHeight(500)
#     proxy.ScanningServer.DwellTime(1e-6)
#
#     Hardware.CCD.value
#     print(proxy.AcquisitionManager.IsAcquisitionHardware(Hardware.Scanning.value))
#
#     proxy.AcquisitionManager.SelectSetup("Acquire Image")
#     proxy.AcquisitionManager.SetAnnotationDisplay('Scanning Search')
#
#     if proxy.AcquisitionManager.CanStart():
#         proxy.AcquisitionManager.Start()
#
#     if proxy.AcquisitionManager.CanStop:
#         proxy.AcquisitionManager.Stop()


if __name__ == "__main__":
    import ESVision
    from AcquisitionServers import AcquireModes

    from enums import *

    import logging
    import numpy as np

    logging.basicConfig(level=logging.INFO)

    with xmlrpc.client.ServerProxy("http://172.16.181.144:8001/tia") as esv:


    #ESVision.Hardware(4)
    #esv = ESVision.Application()
        esv.AcquisitionManager.SetAnnotationDisplay('Scanning Preview', 'Preview BF Scanning Display1')
        esv.AcquisitionManager.SetAcquireAnnnotation((-800e-9,5e-6, 0, 0))

        logging.info(esv.AcquisitionManager.SignalNames())
        type = esv.AcquisitionManager.SignalType('EDX')

        #logging.info(f'')
        logging.info(esv.ScanningServer.SeriesSize(100))

        logging.info(esv.ScanningServer.AcquireMode(AcquireModes(1).name))

        #for x in np.linspace(0, 1e-6, 10):
        #    for y in np.linspace(0, 1e-6, 10):
                #esv.ScanningServer.BeamPosition((x.item(),y.item()))
                #logging.info(esv.ScanningServer.BeamPosition())

        logging.info(ESVision.Signals[type])
        logging.info(esv.ScanningServer.BeamPosition())

        #esv.AcquisitionManager.UnlinkAllSignals()

    #proxy.Stop()
    #multicall = MultiCall(proxy)
    #multicall.AcquisitionManager()
    #ulticall.Start()
    #add_result, address = multicall()

    #proxy.Start()
