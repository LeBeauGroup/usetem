from comtypes.client import CreateObject, Constants
#from comtypes.gen import ESVision as

import esvision

import logging
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

logging.basicConfig(level=logging.INFO)

# Restrict to a particular path.

class TiaService():
    Application = CreateObject("ESVision.Application")
    AcquisitionManager = Application.AcquisitionManager()
    PEELSServer = Application.PEELSServer()
    ScanningServer = Application.ScanningServer()

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/tia',)

# Create server

if __name__ == "__main__":

    with SimpleXMLRPCServer(('172.16.181.144', 8001),
                            requestHandler=RequestHandler, allow_none=True) as server:
        server.register_introspection_functions()
        server.register_instance(esvision.Application(), allow_dotted_names=True)
        server.register_multicall_functions()

        logging.info('Server registered')
        logging.info('Use Control-C to exit')

        # Run the server's main loop
        server.serve_forever()
