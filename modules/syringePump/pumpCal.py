
import numpy as np

def pumpCal(par,ratioReq,Rate,time):

    concFe = par['Fe']

    concOH = par['OH']

    pH = par['initialpH']

    concH = 10**(-pH)

    volRatio = ((ratioReq*concFe)+concH)/concOH

    factor = 1/(1+volRatio)

    rateFe = factor*Rate

    rateOH = (1-factor)*Rate

    #finalpH = 14-(-np.log10(volRatio*concFe*ratioReq-(3*concFe*rateFe*time)-(concH*rateFe*time)))

    return rateFe,rateOH


# par = dict()
# par['Fe'] = 0.3 *10**-3
#
# par['OH'] = 4.53*10**-3
#
# par['initialpH'] = 2.25
#
#
# rateFe,rateOH,finalpH = pumpCal(par,15.2,240,0.5)
#
# rateFe
#
# finalpH
