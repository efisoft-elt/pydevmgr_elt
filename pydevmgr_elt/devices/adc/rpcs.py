from pydevmgr_elt.base import EltDevice
from pydevmgr_elt.devices.motor import Motor

from enum import Enum
Base = EltDevice.Rpcs

R = Base.Rpc # Base Node
RC = R.Config
RPC_ERROR = Motor.Rpcs.RPC_ERROR


class AdcRpcs(Base):
    RPC_ERROR = RPC_ERROR

    class Config(Base.Config):
        rpcDisable:   RC  =  RC(suffix="RPC_Disable")
        rpcEnable:    RC  =  RC(suffix="RPC_Enable")
        rpcReset:     RC  =  RC(suffix="RPC_Reset")
        rpcInit:      RC  =  RC(suffix="RPC_Init")
        rpcMoveAbs:   RC  =  RC(suffix="RPC_MoveAbs",     arg_parsers=["UaInt16",  float,   float])
        rpcMoveRel:   RC  =  RC(suffix="RPC_MoveRel",     arg_parsers=["UaInt16",  float,   float])
        rpcMoveVel:   RC  =  RC(suffix="RPC_MoveVel",     arg_parsers=["UaInt16",  float])
        rpcMoveAngle: RC  =  RC(suffix="RPC_MoveAngle",   arg_parsers=[float])
        rpcStartTrack:RC  =  RC(suffix="RPC_StartTrack",  arg_parsers=[float])
        rpcStopTrack: RC  =  RC(suffix="RPC_StopTrack")
        rpcStop:      RC  =  RC(suffix="RPC_Stop")
        rpcReset:     RC  =  RC(suffix="RPC_Reset")
        rpcInit:      RC  =  RC(suffix="RPC_Init")
            
        


if __name__ == "__main__":
    AdcRpcs()
    print("OK")


