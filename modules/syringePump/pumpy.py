

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
        self.serialcon = Chain(chain)
        self.address = '{0:02.0f}'.format(address)

    def write(self,command):
        self.serialcon.write(str.encode(command + '\r'))

    def infuse(self):
        self.write('irun')

    def oppInfuse(self):
        self.write('rrun')

    def stop(self):
        self.write('stop')

    def setDiameter(self,diameter):

        self.write('diameter '+str(diameter))

    def setFlowRate(self,rate,unit):

        self.write('irate '+str(rate)+' '+unit)

    def time(self, value=None):

        if value is None:
            pass#return self.write('ttime')

        else:
            self.write('ttime '+str(value))

    def setTime(self,time):

        ## here time is in seconds

        self.write('ttime '+str(time))

    def setVolume(self,volume,unit):

        self.write('tvolume '+str(volume)+' '+unit)
