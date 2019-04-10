# @Author: abinashkumar
# @Date:   2019-04-10T17:49:52-04:00
# @Last modified by:   abinashkumar
# @Last modified time: 2019-04-10T17:59:57-04:00



import pumpy
from pumpAddress import pumpAdd

import logging
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# import socket
#
# IP = socket.gethostname()

logging.basicConfig(level=logging.INFO)

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/pump',)

# Create server
for add in pumpAdd:
    print(add)


if __name__ == "__main__":
    server = SimpleXMLRPCServer(('10.154.28.136', 8000),requestHandler=RequestHandler, allow_none=True)

    #with SimpleXMLRPCServer(('10.154.7.25', 8000),requestHandler=RequestHandler, allow_none=True) as server:
    server.register_introspection_functions()
    server.register_instance(pumpy.Pump(pumpAdd), allow_dotted_names=True)
    server.register_multicall_functions()

    logging.info('Server registered')
    logging.info('Use Control-C to exit')

    # Run the server's main loop
    server.serve_forever()
