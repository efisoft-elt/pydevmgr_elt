""" Not a device but define some share methods end constant for tracking devices """
from pydevmgr_core import NodeAlias, NodeVar

from ..base.eltdevice import  GROUP, EltDevice
from ..base.tools import  enum_group, enum_txt,EnumTool
from .motor import Motor, ERROR, MotorRpcInterface

from enum import Enum
##### ############
# SUBSTATE
class SUBSTATE(EnumTool, int, Enum):
    NONE =  0

    NOTOP_NOTREADY =  100
    NOTOP_READY = 101
    NOTOP_INITIALIZING = 102
    NOTOP_ABORTING = 107
    NOTOP_RESETTING = 109
    NOTOP_ENABLING = 110
    
    NOTOP_ERROR =  199

    OP_DISABLING 	= 205
    OP_STANDSTILL	= 216
    OP_MOVING		= 217
    OP_SETTING_POS	= 218
    OP_STOPPING		= 219
    OP_TRACKING		= 220
    OP_PRESETTING	= 221

    OP_ERROR =299
    
    UNREGISTERED = -9999
    
enum_group({
    SUBSTATE.NOTOP_NOTREADY     :  GROUP.NOK, 
    SUBSTATE.NOTOP_READY        :  GROUP.NOK,
    SUBSTATE.NOTOP_INITIALIZING :  GROUP.BUZY, 
    SUBSTATE.NOTOP_ABORTING     :  GROUP.BUZY, 
    SUBSTATE.NOTOP_RESETTING    :  GROUP.BUZY, 
    SUBSTATE.NOTOP_ENABLING     :  GROUP.BUZY, 
    SUBSTATE.NOTOP_ERROR        :  GROUP.ERROR, 
    SUBSTATE.OP_DISABLING 	    :  GROUP.BUZY, 
    SUBSTATE.OP_STANDSTILL	    :  GROUP.OK,
    SUBSTATE.OP_MOVING		    :  GROUP.BUZY, 
    SUBSTATE.OP_SETTING_POS	    :  GROUP.BUZY, 
    SUBSTATE.OP_STOPPING		:  GROUP.BUZY, 
    SUBSTATE.OP_TRACKING		:  GROUP.OK, 
    SUBSTATE.OP_PRESETTING	    :  GROUP.BUZY, 
    SUBSTATE.OP_ERROR           :  GROUP.ERROR,   
    })


### ##############
# ERROR
ERROR = Motor.ERROR


### ##############
# RPC error
RPC_ERROR = MotorRpcInterface.RPC_ERROR

class MODE(int, Enum):
    pass
    
class TrkStatInterface(EltDevice.StatInterface):    
    ERROR = ERROR
    MODE = MODE
    SUBSTATE = SUBSTATE
    
    @NodeAlias.prop("track_mode_txt", ["track_mode"])
    def track_mode_txt(self, track_mode: int) -> str:
        return self.MODE(track_mode).name
    
    @NodeAlias.prop("is_moving", ["substate"])
    def is_moving(self, substate: int) -> bool:
        """ -> True is axis is moving """
        return substate == self.SUBSTATE.OP_MOVING

    @NodeAlias.prop("is_standstill", ["substate"])
    def is_standstill(self,  substate: int) -> bool:
        """ -> True is axis is standstill """
        return substate == self.SUBSTATE.OP_STANDSTILL
    
    @NodeAlias.prop("is_presetting", ["substate"])
    def is_presetting(self,  substate: int) -> bool:
        """ -> True is axis is preseting """
        return substate == self.SUBSTATE.OP_PRESETTING
    
    @NodeAlias.prop("is_tracking", ["substate"])
    def is_tracking(self,  substate: int) -> bool:
        """ -> True is axis is tracking """
        return substate == self.SUBSTATE.OP_TRACKING

    
class Trk:
    # note start_track not defined here 
    # because specific (Adc.start_track take one arg Drot.start_track two)        
    def stop_track(self) -> None:
        self.rpc.rpcStopTrack.rcall()


class TrkStatData(EltDevice.Data.StatData):   
    track_mode: NodeVar[int] = 0  
    track_mode_txt: NodeVar[str] = ""
    is_moving: NodeVar[bool] = False
    is_standstill : NodeVar[bool] = False 
    is_presetting : NodeVar[bool] = False
    is_tracking: NodeVar[bool] = False 