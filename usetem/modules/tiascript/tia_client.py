import xmlrpc.client
from xmlrpc.client import MultiCall, Boolean



if __name__ == "__main__":
    import esvision
    #from AcquisitionServers import AcquireModes

    from enums import *
    import pickle

    import logging
    import numpy as np

    logging.basicConfig(level=logging.INFO)

    with xmlrpc.client.ServerProxy("http://172.16.181.144:8001/tia") as prox:

        #test = pickle.loads(prox.ActiveDisplayWindow(),  encoding='bytes')
        data = prox.ActiveDisplayWindow().data

        print(pickle.loads(data,encoding='ASCII').name)

    #ESVision.Hardware(4)
    #esv = ESVision.Application()
        # esv.AcquisitionManager.SetAcquireAnnnotation((-800e-9,5e-6, 0, 0))
        #
        # logging.info(esv.AcquisitionManager.SignalNames())
        # type = esv.AcquisitionManager.SignalType('EDX')

        #logging.info(f'')

        #esv.AcquisitionManager.UnlinkAllSignals()

    #proxy.Stop()
    #multicall = MultiCall(proxy)
    #multicall.AcquisitionManager()
    #ulticall.Start()
    #add_result, address = multicall()

    #proxy.Start()
