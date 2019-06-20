



#'/dev/tty.usbmodemD304001'

address = '/dev/tty.usbmodem26211'

import serial
import argparse
import logging


class Chain(serial.Serial):

    def __init__(self, port):
        serial.Serial.__init__(self,port=port, stopbits=serial.STOPBITS_TWO, parity=serial.PARITY_NONE, timeout=2)
        self.flushOutput()
        self.flushInput()
        logging.info('Chain created on %s',port)


class pHMeter:

    def __init__(self, chain, address=0, name='Pump 11'):
        self.name = name

        self.serialcon = []

        self.serialcon = Chain(chain)

        self.address = '{0:02.0f}'.format(address)

    def write(self,command):
        self.serialcon.write(str.encode(command + '\r'))


pHMain = pHMeter(address)

temp = pHMain.serialcon.write(str.encode('SETMODE PH' + '\r'))
temp

temp = pHMain.serialcon.write(str.encode('GETMEAS 1\r'))
temp
bytesToRead = pHMain.serialcon.inWaiting()
bytesToRead

pHMain.serialcon.readline()


'\n\r------------------------------\n\r\n\rThermo Scientific (c) 2011\n\rA211 pH\n\rMeter S/N                X49401\n\rSW Rev                   3.04\n\rUser ID  ABCDE\n\r04/19/19 07:09:14\n\r\n\rpH                       6.70 pH\n\rmV                       11.7 mV\r\n\rTemperature              25.0 C\r\n\rSlope                    86.4 %\n\rMethod#                  M100 \n\rCalibration              #1 \r\n\r\n\rOperator_______________\n\rSignature_______________\n\r\r>'
pHMain.serialcon
pHMain.
