

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

    def infuse(self,num):
        self.write('irun',num)

    def oppInfuse(self,num):
        self.write('rrun',num)

    def stop(self,num):
        self.write('stop',num)

    def setDiameter(self,diameter,num):

        self.write('diameter '+str(diameter),num)

    def setFlowRate(self,rate,unit,num):

        self.write('irate '+str(rate)+' '+unit,num)

    def time(self,value,num):

        if value is None:
            pass#return self.write('ttime')

        else:
            self.write('ttime '+str(value),num)

    def setTime(self,time,num):

        ## here time is in seconds

        self.write('ttime '+str(time),num)

    def setVolume(self,volume,unit,num):

        self.write('tvolume '+str(volume)+' '+unit,num)
