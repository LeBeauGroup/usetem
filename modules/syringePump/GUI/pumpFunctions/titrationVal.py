

import xlrd

from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy as np


book = xlrd.open_workbook('pumpFunctions\TitrationCurve.xlsx')

sheet = book.sheet_by_index(0)

RatioOHFE = [sheet.cell_value(r,3) for r in range(sheet.nrows)][3:72]

pHOHFE = [sheet.cell_value(r,4) for r in range(sheet.nrows)][3:72]


RatioOHFEAS = [sheet.cell_value(r,8) for r in range(sheet.nrows)][3:51]

pHOHFEAS = [sheet.cell_value(r,9) for r in range(sheet.nrows)][3:51]




# for t in enumerate(temp):
#     print(t)
#
# np.where(np.array(RatioOHFE)==np.array(temp)[-1])

def removeDuplicate(RatioOHFE,pHOHFE):

    temp =np.sort(list(set(RatioOHFE)))

    RatioOHFEmod = np.zeros(len(temp))
    pHOHFEmod = np.zeros(len(temp))


    tSet = [np.where(np.array(RatioOHFE)==t) for t in temp]



    count = 0

    for i in tSet:
        #print(i[0][0])

        if len(i[0]) == 1:
            RatioOHFEmod[count] = RatioOHFE[i[0][0]]
            pHOHFEmod[count] = pHOHFE[i[0][0]]


        elif len(i[0]) > 1:

            tempRatio =[]
            temppH = []

            for j in i[0]:

                tempRatio.append(RatioOHFE[j])

                temppH.append(pHOHFE[j])

            RatioOHFEmod[count] = np.mean(tempRatio)

            pHOHFEmod[count] = np.mean(temppH)


        count +=1

    return RatioOHFEmod,pHOHFEmod



RatioOHFEnew,pHOHFEnew = removeDuplicate(RatioOHFE,pHOHFE)

RatioOHFEASnew,pHOHFEASnew = removeDuplicate(RatioOHFEAS,pHOHFEAS)


funcFE = interp1d(np.array(RatioOHFEnew),np.array(pHOHFEnew),kind='cubic')

funcFEAS = interp1d(np.array(RatioOHFEASnew),np.array(pHOHFEASnew),kind='cubic')

xRatio = np.arange(RatioOHFEnew.min(),RatioOHFEnew.max(),0.1)

ypHFE = funcFE(xRatio)

xRatioAS = np.arange(RatioOHFEASnew.min(),RatioOHFEASnew.max(),0.1)

ypHFEAS = funcFEAS(xRatioAS)

np.save('titration/ratioOH_FE',np.around(xRatio,2))
np.save('titration/pHOH_FE',np.around(ypHFE,2))
np.save('titration/ratioOH_FEAS',np.around(xRatioAS,2))
np.save('titration/pHOH_FEAS',np.around(ypHFEAS,2))
