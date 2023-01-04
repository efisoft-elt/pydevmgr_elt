from pydevmgr_elt.base import EltDevice
from pydevmgr_elt.base.tools import enum_txt

from enum import Enum
Base = EltDevice.Rpcs

R = Base.Rpc # Base Node
RC = R.Config

### ##############
# RPC error
class RPC_ERROR(int, Enum):
    OK =  0
    NOT_OP =  -1
    NOT_NOTOP_READY =  -2
    NOT_NOTOP_NOTREADY = -3
    LOCAL =  -4
    SW_LIMIT_LOWER = -5
    SW_LIMIT_UPPER = -6
    INIT_WHILE_MOVING = -7
    
    UNREGISTERED = -9999
    
enum_txt ( {
    RPC_ERROR.OK:					 'OK',
    RPC_ERROR.NOT_OP:				 'Cannot control motor. Not in OP state.',
    RPC_ERROR.NOT_NOTOP_READY:	     'Call failed. Not in NOTOP_READY.',
    RPC_ERROR.NOT_NOTOP_NOTREADY:	 'Call failed. Not in NOTOP_NOTREADY/ERROR.',
    RPC_ERROR.LOCAL:				 'RPC calls not allowed in Local mode.',
    RPC_ERROR.SW_LIMIT_LOWER:		 'Move rejected. Target Pos < Lower SW Limit',
    RPC_ERROR.SW_LIMIT_UPPER:		 'Move rejected. Target Pos > Upper SW Limit',
    RPC_ERROR.INIT_WHILE_MOVING:	 'Cannot INIT moving motor. Motor stopped. Retry.',
    
    RPC_ERROR.UNREGISTERED:          'Unregistered RPC Error',
})



class MotorRpcs(Base):
    RPC_ERROR = RPC_ERROR

    class Config(Base.Config):
        rpcDisable: RC = RC(suffix= 'RPC_Disable')
        rpcEnable: RC = RC(suffix= 'RPC_Enable')
        rpcInit: RC = RC(suffix= 'RPC_Init')
        rpcMoveAbs: RC = RC(suffix= 'RPC_MoveAbs', arg_parsers=['Float', 'Float'] )
        rpcMoveRel: RC = RC(suffix= 'RPC_MoveRel', arg_parsers=['Float', 'Float'] )
        rpcMoveVel: RC = RC(suffix= 'RPC_MoveVel', arg_parsers=['Float'] )
        rpcReset: RC = RC(suffix= 'RPC_Reset')
        rpcStop: RC = RC(suffix= 'RPC_Stop')



 


