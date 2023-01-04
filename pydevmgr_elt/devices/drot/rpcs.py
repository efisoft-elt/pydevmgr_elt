from pydevmgr_elt.devices.motor import Motor
from pydevmgr_elt.devices.drot.stat import MODE
from pydevmgr_ua import UaInt16

from enum import Enum
Base = Motor.Rpcs

R = Base.Rpc # Base Node
RC = R.Config

to_int16 = UaInt16().parse

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
        rpcMoveAngle : RC = RC(suffix="RPC_MoveAngle", arg_parsers=[float])
        rpcStartTrack: RC = RC(suffix="RPC_StartTrack", arg_parsers=[mode_parser, float])
         
        rpcStopTrack: RC = RC(suffix="RPC_StopTrack")


