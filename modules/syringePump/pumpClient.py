# @Author: abinashkumar
# @Date:   2019-03-26T18:45:38-04:00
# @Last modified by:   abinashkumar
# @Last modified time: 2019-04-10T18:03:31-04:00



import xmlrpc.client
#from xmlrpc.client import MultiCall, Boolean

import pumpy

import logging
import numpy as np
import pumpCal

intParam  = dict()

intParam['Fe'] = 0.3*10**-3
intParam['OH'] = 4.53*10**-3
intParam['initialpH'] = 2.25

reqRatio = 15.2
rate = 240
time = 5

rateFe,rateOH = pumpCal.pumpRate(intParam,reqRatio,rate,time)



if __name__ == "__main__":


    logging.basicConfig(level=logging.INFO)

    prox = xmlrpc.client.ServerProxy("http://10.154.28.136:8000/pump")

    prox.setFlowRate(rateFe,'ul/min',0)

    prox.setFlowRate(rateOH,'ul/min',1)


    prox.setVolume(1000,'ul',0)
    prox.time(10)
    prox.infuse()
    #prox.oppInfuse()

    #p1.setVolume(10,'ml')
