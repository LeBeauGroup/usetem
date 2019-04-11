# @Author: abinashkumar
# @Date:   2019-03-26T18:45:38-04:00
# @Last modified by:   abinashkumar
# @Last modified time: 2019-04-11T00:49:27-04:00



import xmlrpc.client
#from xmlrpc.client import MultiCall, Boolean
import pumpy
import logging
import numpy as np
import pumpCal

### For initial parameters to set the rate

intParam  = dict()

intParam['Fe'] = 0.3*10**-3
intParam['OH'] = 4.53*10**-3
intParam['initialpH'] = 2.25

reqRatio = 15.2   ## setting required ratio of moles of OH/Fe ions required for the reaction
rate = 240        ## total rate
time = 5          ## time for which pump need to be run

rateFe,rateOH = pumpCal.pumpRate(intParam,reqRatio,rate,time) ## calculating the rate required for different pumps



if __name__ == "__main__":


    logging.basicConfig(level=logging.INFO)

    prox = xmlrpc.client.ServerProxy("http://10.154.28.136:8000/pump")

    prox.FlowRate(rateFe,'ul/min',0)

    prox.FlowRate(rateOH,'ul/min',1)


    prox.Volume(1000,'ul',0)
    prox.time(10)
    prox.infuse()
    

    #p1.setVolume(10,'ml')
