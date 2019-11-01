from useTEM.modules.temscript.instrument import Instrument
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

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/temscript',)

# Create server

if __name__ == "__main__":

    with SimpleXMLRPCServer(('127.0.0.1', 8001),
                            requestHandler=RequestHandler, allow_none=True) as server:
        server.register_introspection_functions()

        server.register_instance(Instrument(), allow_dotted_names=True)
        server.register_multicall_functions()

        logging.info('Server registered')
        logging.info('Use Control-C to exit')

        # Run the server's main loop
        server.serve_forever()
