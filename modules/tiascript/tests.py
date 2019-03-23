#!/usr/bin/env python3


if __name__ == "__main__":
    import application
    import logging
    import pickle
    import matplotlib.pyplot as plt
    logging.basicConfig(level=logging.INFO)

    #ESVision.Hardware(4)
    esv = application.Application()
    #esv.AcquisitionManager.SetAnnotationDisplay('Scanning Search', 'Search BF Scanning Display1')
    #esv.AcquisitionManager.SetAcquireAnnnotation((-800e-9,5e-6, 0, 0))

    #logging.info(esv.AcquisitionManager.SignalNames())
    bc = esv.BeamControl

    print(esv.createNewImageDisplay((256,24)))

    esv.activeDisplayWindow()
    #path = 'Scanning Search/Search HAADF Scanning Display1/Search HAADF'
    path = 'Display Window 52/display/display'
    obj = esv.findDisplayObject(path)


    foundObject = pickle.loads(obj.data)['data']
    #plt.imshow(foundObject)
    #plt.show()


#
#
# ss = esv.ScanningServer
# names = ss.MagnificationNames('Imaging')
#  d
#
# ss.ReferencePosition((0,1))
# print(ss.MagnificationName(1, 'Imaging'))
#
# ss.CreateMagnification(800, (0, 0, 1, 1),  'Imaging')
#
# ss.DeleteMagnification('800 X',  'Imaging')
#
# bc.PositionCalibrated(False)
# #bc.SetLineScan((-1,0),(0,1), 100)
#
# bc.SetFrameScan((0.0,0.0, 1.0,1.0), 100, 100)
#
#
# bc.SetContinuousScan()
# bc.DwellTime(1e-5)
# bc.Start()
#
# #bc.Stop()