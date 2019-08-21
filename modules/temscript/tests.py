#!/usr/bin/env python3

import numpy as np

if __name__ == "__main__":

    from launch.modules.temscript import instrument as instrument

    #import instrument
    from launch.modules.temscript import enums
    import logging
    import pickle
    import utilities
    import matplotlib.pyplot as plt

    logging.basicConfig(level=logging.INFO)

    instrument = instrument.Instrument()
    # instrument.acquisition.addDetectorByName('DF4')
    # instrument.acquisition.stemDetectors.dwellTime(1e-7)
    # instrument.acquisition.stemDetectors.setFrameSize(AcqFrameSize.Full)
    # instrument.acquisition.stemDetectors.setMaxFrameSize(AcqMaxFrame.Full)

    pos = utilities.positionDict(1e-6,1e-5,1e-5, 0, 0)
    #print(instrument.stage.goto(pos, 1|2|3))


    # print(instrument.acquisition.stemDetectors())

    #print(instrument.vacuum.runBufferCycle())
    # instrument.projection.mode(ProjMode.Imaging.value)
    #instrument.projection.defocus(1e-8)


    # need to chedk
    deltaArray = [-1e-6, 1e-5, 5e-6, 4*np.pi/180, 0]
    instrument.stage.goto(deltaArray, enums.StageAxes.axisA.value|enums.StageAxes.axisXY.value)
    # instrument.projection.lensProgram(ProjLensProg.Regular.value)

    # print(instrument.gun.htValue(216230))
    #print(instrument.mode(InstrumentMode.TEM.value))
    #print(instrument.projection.normalize(ProjNormalization.All.value))
    #print(instrument.camera.mainScreenPosition(0))




    # plt.imshow(instrument.acquisition.acquireImages()[0])
    # plt.show()
