#!/usr/bin/env python3


if __name__ == "__main__":
    import application
    import logging
    import pickle
    import numpy as np
    import matplotlib.pyplot as plt
    logging.basicConfig(level=logging.INFO)

    #ESVision.Hardware(4)
    esv = application.Application()
    #esv.AcquisitionManager.SetAnnotationDisplay('Scanning Search', 'Search BF Scanning Display1')
    #esv.AcquisitionManager.SetAcquireAnnnotation((-800e-9,5e-6, 0, 0))

    #logging.info(esv.AcquisitionManager.SignalNames())
    bc = esv.BeamControl
#    bc.Stop()
    #print(esv.createNewImageDisplay((512,512)))

    activeName = esv.activeDisplayWindow()

    #objectPath = f'{activeName}/real/real'
    objectPath = 'Scanning Search/Search DF4 Scanning Display1/Search DF4'


    newDisplay = esv.createNewImageDisplay((512,512))

    esv.findDisplayObject(f'{newDisplay}/real/real')

    acq = esv.AcquisitionManager


    acq.AddSetup('Full')



    acq.AddSetup('Focus')
    #ss = esv.ScanningServer
    #bc.PositionCalibrated(False)

    #bc.SetFrameScan((0,0, 0.5, 0.5), 100,100)

    #acq.SelectSetup('testing')
    acq.LinkSignal('Analog3', objectPath)


    #acq.SelectSetup('testing')

    # positions = list()
    # numPos = 100
    # radius = 0.25

    # for index in range(0,numPos):
    #     x = radius *  np.cos(2 * np.pi * index / numPos)
    #     y = radius *  np.sin(2 * np.pi * index / numPos)
    #
    #     positions.append((x,y))
    #
    #     print(positions)

#     bc.LoadPositions(positions)
#     bc.DwellTime(5e-6)
#     bc.SetContinuousScan()
#
# #    print(acq.SignalNames())
#
#     print(bc.IsScanning())
#
#     if bc.IsScanning():
#         bc.Stop()
#         bc.MoveBeam(0,0)
#         bc.Start()
#     else:
#         bc.Start()

    #bc.Stop()
    # print(bc.IsScanning())
    #esv.activeDisplayWindow()






    #foundObject = pickle.loads(obj.data)['data']
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
