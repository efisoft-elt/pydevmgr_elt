from pydevmgr_core import  NodeAlias1, Defaults 
from pydevmgr_elt.base import EltDevice,  GROUP
from pydevmgr_elt.devices.motor import Motor
from pydevmgr_elt.devices.drot.stat import MODE
from pydevmgr_elt.base.tools import _inc, enum_group, enum_txt
from pydevmgr_ua import UaInt16

from enum import Enum
Base = Motor.Rpcs

R = Base.Rpc # Base Node
RC = R.Config
RD = Defaults[RC] # this typing var says that it is a Rpc object holding default values 

to_int16 = UaInt16()

# RPC_ERROR are iddentical to Motor 

class TRACK_MODE(int, Enum):
    SKY  = MODE.SKY.value 
    ELEV = MODE.ELEV.value 
        

def mode_parser(mode):
    if isinstance(mode, str):
        try:
            mode = getattr( TRACK_MODE, mode)
        except AttributeError:
            choices = ",".join(str(m) for m in  TRACK_MODE)
            raise ValueError(f'tracking mode must be one of {choices} got %r'%mode)
    else:
        mode = TRACK_MODE(mode)
    return to_int16(mode)


class DrotRpcs(Base):

    class Config(Base.Config):
        rpcMoveAngle : RD = RC(suffix="RPC_MoveAngle", arg_parsers=[float])
        rpcStartTrack: RD = RC(suffix="RPC_StartTrack", arg_parsers=[mode_parser, float])
         
        rpcStopTrack: RD = RC(suffix="RPC_StopTrack")


