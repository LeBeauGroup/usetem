from comtypes.client import CreateObject, Constants
from comtypes.client import GetModule

esvisionlib = GetModule("C:\\Program Files (x86)\\FEI\\TIA\\Bin\\ESVision.tlb")
from comtypes.gen.ESVision import Position2D

import comtypes
import comtypes.server.localserver

class Position2DImpl(Position2D):
    # registry entries
    _reg_threading_ = "Both"
    _reg_progid_ = "ESVision.Position2D.1"
    _reg_novers_progid_ = "ESVision.Position2D"
    _reg_desc_ = "Simple COM server for testing"
    _reg_clsctx_ = comtypes.CLSCTX_INPROC_SERVER | comtypes.CLSCTX_LOCAL_SERVER
    _regcls_ = comtypes.server.localserver.REGCLS_MULTIPLEUSE

if __name__ == "__main__":
    from comtypes.server.register import UseCommandLine
    UseCommandLine(Position2DImpl)
