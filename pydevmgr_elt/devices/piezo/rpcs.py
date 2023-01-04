from pydevmgr_elt.base import EltDevice
from pydevmgr_elt.base.tools import  enum_txt

from enum import Enum
Base = EltDevice.Rpcs

R = Base.Rpc # Base Node
RC = R.Config

### ##############
# RPC error
class RPC_ERROR(int, Enum):
    OK			                =  0
    NOT_OP                      = -1
    NOT_NOTOP_READY		        = -2
    NOT_NOTOP_NOTREADY          = -3
    MOVING_USER                 = -5
    MOVING_BIT                  = -6
    LOCAL                       = -7
    
    UNREGISTERED = -9999

# Add text definition to each constants, the definition is then accessible throught .txt attribute 
enum_txt ({
    RPC_ERROR.OK:						 'OK',
    RPC_ERROR.NOT_OP:					 'Cannot control device. Not in OP state.',
    RPC_ERROR.NOT_NOTOP_READY:		     'Call failed. Not in NOTOP_READY.',
    RPC_ERROR.NOT_NOTOP_NOTREADY:		 'Call failed. Not in NOTOP_NOTREADY/ERROR.',
    RPC_ERROR.LOCAL:					 'RPC calls not allowed in Local mode.',
    RPC_ERROR.MOVING_USER:			     'Set user value out of range.',
    RPC_ERROR.MOVING_BIT:				 'Set bit value out of range.',
    
    RPC_ERROR.UNREGISTERED:          'Unregistered RPC Error',
    })



class PiezoRpcs(Base):
    RPC_ERROR = RPC_ERROR

    class Config(Base.Config):
        rpcAuto: RC = RC(suffix= 'RPC_Auto')
        rpcDisable: RC = RC(suffix= 'RPC_Disable')
        rpcEnable: RC = RC(suffix= 'RPC_Enable')
        rpcHome: RC = RC(suffix= 'RPC_Home')
        rpcInit: RC = RC(suffix= 'RPC_Init')
        rpcMoveBits: RC = RC(suffix= 'RPC_MoveBit', arg_parsers=['UaInt16', 'UaInt16', 'UaInt16'] )
        rpcMoveUser: RC = RC(suffix= 'RPC_MoveUser', arg_parsers=['Float', 'Float', 'Float'] )
        rpcPos: RC = RC(suffix= 'RPC_Pos')
        rpcReset: RC = RC(suffix= 'RPC_Reset')
        rpcStop: RC = RC(suffix= 'RPC_Stop')
 


