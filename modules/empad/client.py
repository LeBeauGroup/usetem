import xmlrpc.client
from xmlrpc.client import MultiCall, Boolean
import sys

if __name__ == "__main__":
    import pickle
    import logging
    import numpy as np

    logging.basicConfig(level=logging.INFO)

    with xmlrpc.client.ServerProxy('http://192.168.6.6:8000/empad') as prox:
        prox.test('connected')
        prox.connect_to_server()



    #proxy.Stop()
    #multicall = MultiCall(proxy)
    #multicall.AcquisitionManager()
    #ulticall.Start()
    #add_result, address = multicall()

    #proxy.Start()
