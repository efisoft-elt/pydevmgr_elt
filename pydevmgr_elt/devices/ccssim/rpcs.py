from pydevmgr_elt.base import EltDevice
from pydevmgr_elt.base.tools import  enum_txt

from enum import Enum
Base = EltDevice.Interface

R = Base.Rpc # Base Node
RC = R.Config


class RPC_ERROR(int, Enum):
    
    UNREGISTERED = -9999
    
enum_txt ({ # copy past on MgetRpcErrorTxt in PLC
          
        RPC_ERROR.UNREGISTERED:          'Unregistered RPC Error',
})



class CcsSimRpcs(Base):
    RPC_ERROR = RPC_ERROR
    
    class Config(Base.Config):
        rpcSetCoordinates:  RC = RC(suffix="RPC_SetCoordinates", arg_parsers=[float, float, float])


