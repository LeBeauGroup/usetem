import logging
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

logging.basicConfig(level=logging.INFO)


import socket

# Function to display hostname and
# IP address
def get_Host_name_IP():
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        #print("IP : ",host_ip)
    except:
        print("Unable to get Hostname and IP")

    return host_ip

# Driver code
 #Function call

# Restrict to a particular path.

class EmpadServer():

    def __init__(self,serial_address = '/dev/ttyS4'):

        self.serial_address = serial_address #serial address of Keithley on current EMPAD computer, last updated 6/12/2018

        try:
            ser = serial.Serial(self.serial_address, timeout = 1)
            ser.write('*RST\r')
            ser.write(':SOUR:FUNC VOLT\r')
            ser.write(':SOUR:VOLT:RANG:AUTO 1\r')
            ser.write(':SOUR:VOLT:LEV 120\r')
            ser.write(':SENS:CURR:PROT 200E-6\r')
            ser.write(':SENS:FUNC "CURR"\r')
            ser.write(':SENS:CURR:RANG:AUTO 1\r')
            ser.write(':ARM:COUN INF\r')
            ser.write(':OUTP ON\r')
            ser.write(':INIT\r')

            keithley_connected = True
        except:
            keithley_connected = False


    def connect_to_server(self):
        server_address = (self.serverpop.ip, int(self.serverpop.port))
        global sock
        global connected
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        if self.serverpop.connected:
            try:
                sock.close()
                self.serverpop.connected = False
                connected = False
            except:
                self.serverpop.connected = False
                connected = False
        else:
            try:
                sock.connect(server_address)
                self.serverpop.connected = True
                connected = True
                Send_to_Cam(('ldcmndfile empadstart_p2_01_2017_06_07.cmd\n'))

                Send_to_Cam(('padcom roimask annulus_lr_ud_ 0 64 64 20 64\n'))

                Send_to_Cam(('filestore 1 5\n'))

                Send_to_Cam(('padcom roimask box_lr_ud_ 1 64 64 2 2\n'))

            except Exception as e:
                print(e)
                self.serverpop.connected = True
                self.serverpop.connected = False #need to change to update related attributes
                connected = False

    def Send_to_Cam(self,msg, recvflag = True):
        if not connected:
            raise Exception('NOT CONNECTED')
            return
        msg = msg.encode()

        sock.sendall(msg)
        if recvflag:
            print(sock.recv(4096).decode())

        time.sleep(0.010)

    def test(self,msg):
        print(msg)

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/empad',)

# Create server

if __name__ == "__main__":

    with SimpleXMLRPCServer(('172.16.208.147', 8001),
                            requestHandler=RequestHandler, allow_none=True) as server:
        server.register_introspection_functions()

        test = EmpadServer()
        test.test('blash')
        server.register_instance(EmpadServer(), allow_dotted_names=True)
        server.register_multicall_functions()

        logging.info('Server registered')
        logging.info('Use Control-C to exit')

        # Run the server's main loop
        server.serve_forever()
