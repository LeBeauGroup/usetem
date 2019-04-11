# @Author: abinashkumar
# @Date:   2019-04-10T17:49:52-04:00
# @Last modified by:   abinashkumar
# @Last modified time: 2019-04-11T00:49:43-04:00



### Adapted from pumpy

import serial
import argparse
import logging


class Chain(serial.Serial):

    def __init__(self, port):
        serial.Serial.__init__(self,port=port, stopbits=serial.STOPBITS_TWO, parity=serial.PARITY_NONE, timeout=2)
        self.flushOutput()
        self.flushInput()
        logging.info('Chain created on %s',port)


class Pump:

    def __init__(self, chain, address=0, name='Pump 11'):
        self.name = name

        self.serialcon = []
        for add in chain:
            self.serialcon.append(Chain(add))

        self.address = '{0:02.0f}'.format(address)

    def write(self,command,num):
        self.serialcon[num].write(str.encode(command + '\r'))

    def syrManu(self,type,volume,unit,num):

        self.write('syrm'+'['+type+' '+volume+' '+unit,num)

    def Diameter(self,diameter,num):

        self.write('diameter '+str(diameter),num)

    def FlowRate(self,rate,unit,num):

        ### maximum flow rate is 13.2611 ml/min and minimum 12.7699 nl/min

        self.write('irate '+str(rate)+' '+unit,num)


    def Volume(self,volume,unit,num):

        ### maximum depending on the syringe type

        self.write('tvolume '+str(volume)+' '+unit,num)

    def time(self,value,num):

        if value is None:
            pass#return self.write('ttime')

        else:
            self.write('ttime '+str(value),num)

    def infuse(self,num):
        self.write('irun',num)

    def stop(self,num):
        self.write('stop',num)
