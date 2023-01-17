from pydevmgr_elt.base import EltDevice
from pydevmgr_elt.devices.motor import Motor
from pydevmgr_core import argc

from enum import Enum
Base = EltDevice.Rpcs

R = Base.Rpc # Base Node
RC = R.Config
RPC_ERROR = Motor.Rpcs.RPC_ERROR


posargs = [argc("axis","UaInt16"), argc("pos",float),  argc("vel", float)]

class AdcRpcs(Base):
    RPC_ERROR = RPC_ERROR

    class Config(Base.Config):
        rpcDisable:   RC  =  RC(suffix="RPC_Disable")
        rpcEnable:    RC  =  RC(suffix="RPC_Enable")
        rpcReset:     RC  =  RC(suffix="RPC_Reset")
        rpcInit:      RC  =  RC(suffix="RPC_Init")
        rpcMoveAbs:   RC  =  RC(suffix="RPC_MoveAbs", args=posargs)
        rpcMoveRel:   RC  =  RC(suffix="RPC_MoveRel", args=posargs)
        rpcMoveVel:   RC  =  RC(suffix="RPC_MoveVel", args=[argc("axis","UaInt16"), argc("vel", float)])
        rpcMoveAngle: RC  =  RC(suffix="RPC_MoveAngle",   args=[argc('angle', float)])
        rpcStartTrack:RC  =  RC(suffix="RPC_StartTrack",  args=[argc('angle', float)])
        rpcStopTrack: RC  =  RC(suffix="RPC_StopTrack")
        rpcStop:      RC  =  RC(suffix="RPC_Stop")
        rpcReset:     RC  =  RC(suffix="RPC_Reset")
        rpcInit:      RC  =  RC(suffix="RPC_Init")
            
        


if __name__ == "__main__":
    AdcRpcs()
    print("OK")


