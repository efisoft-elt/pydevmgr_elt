from pydevmgr_core import NodeVar, record_class, Defaults
from pydevmgr_ua import Int16, Int32
from ..base.tools import enum_group, enum_txt, EnumTool
from ..base.eltdevice import EltDevice, GROUP

from enum import Enum

from . import trk
from .motor import Motor

from pydantic import Field 

from ._drot_autobuilt import _Drot


#                      _              _   
#   ___ ___  _ __  ___| |_ __ _ _ __ | |_ 
#  / __/ _ \| '_ \/ __| __/ _` | '_ \| __|
# | (_| (_) | | | \__ \ || (_| | | | | |_ 
#  \___\___/|_| |_|___/\__\__,_|_| |_|\__|
# 

##### ############
# SUBSTATE
SUBSTATE = trk.SUBSTATE

### ##############
# RPC errors
RPC_ERROR = trk.RPC_ERROR

### ##############
# error
ERROR = trk.ERROR

### ############# 
# Mode 

class MODE(EnumTool, int, Enum):
    ENG		= 0
    STAT	= 1
    SKY		= 2
    ELEV	= 3
    USER	= 4

enum_group( {
    MODE.ENG    : GROUP.ENG,
    MODE.STAT	: GROUP.STATIC,
    MODE.SKY    : GROUP.TRACKING,
    MODE.ELEV	: GROUP.TRACKING,
    MODE.USER	: GROUP.TRACKING,
})
    
def mode_parser(mode):
    if isinstance(mode, str):
        if mode not in ['SKY', 'ELEV']:
            raise ValueError('tracking mode must be one of SKY or ELEV got %r'%mode)
        mode = getattr(MODE, mode)
    return Int16(mode)



#  _       _             __                
# (_)_ __ | |_ ___ _ __ / _| __ _  ___ ___ 
# | | '_ \| __/ _ \ '__| |_ / _` |/ __/ _ \
# | | | | | ||  __/ |  |  _| (_| | (_|  __/
# |_|_| |_|\__\___|_|  |_|  \__,_|\___\___|


N = EltDevice.Node
RD = Defaults
CN = EltDevice.Node.Config
CI = EltDevice.Interface.Config
CR = EltDevice.Rpc.Config




class DrotStatInterface(trk.TrkStatInterface, Motor.Stat): 
    ERROR = ERROR
    MODE = MODE
    SUBSTATE = SUBSTATE   
    
    class Config(Motor.Stat.Config):
        track_mode: RD[CN] = CN(suffix="stat.nMode")

    class Data(Motor.Stat.Data, trk.TrkStatData):
        pass


class DrotCfgInterface(Motor.Cfg):
    
    class Config(Motor.Cfg.Config):
        type: str = 'Drot.Cfg'
        dir_sign: RD[CN] = CN(suffix='cfg.nDirSign', parser='UaInt32')
        focus_sign: RD[CN] = CN(suffix='cfg.nFocusSign', parser='UaInt32')
        trk_period: RD[CN] = CN(suffix='cfg.nMinSkipCycles', parser='UaInt32')

    class Data(Motor.Cfg.Data):
        dir_sign: NodeVar[int] = 0
        focus_sign: NodeVar[int] = 0
        trk_period: NodeVar[int] = 0

    # ################
    dir_sign = N.prop()
    focus_sign = N.prop()
    trk_treshold = N.prop()
    

class DrotRpcInterface(Motor.Rpcs): 
    class Config(Motor.Rpcs.Config):
        
        rpcMoveAngle : RD[CR] = CR(suffix="RPC_MoveAbs", arg_parsers=[float])
        rpcStartTrack: RD[CR] = CR(suffix="RPC_StartTrack", arg_parsers=[mode_parser, float])
        
        
    RPC_ERROR = RPC_ERROR
    
 
class DrotData(Motor.Data):
    Cfg = DrotCfgInterface.Data
    cfg: Cfg = Cfg()
    
    Stat = DrotStatInterface.Data
    stat: Stat = Stat()
    
#      _            _          
#   __| | _____   _(_) ___ ___ 
#  / _` |/ _ \ \ / / |/ __/ _ \
# | (_| |  __/\ V /| | (_|  __/
#  \__,_|\___| \_/ |_|\___\___|
#



class DrotConfig(Motor.Config, _Drot.Config):
    type: str = "Drot"
    Cfg =  DrotCfgInterface.Config 
    Rpc =  DrotRpcInterface.Config 
    Stat = DrotStatInterface.Config
    cfg : RD[Cfg] = Cfg() 
    rpc : RD[Rpc] = Rpc() 
    stat : RD[Stat] = Stat() 
   


@record_class
class Drot(Motor, trk.Trk):
    SUBSTATE = SUBSTATE
    MODE = MODE 
    ERROR = ERROR
    
    Config = DrotConfig
    Data = DrotData
    
    Stat = DrotStatInterface
    Cfg  = DrotCfgInterface
    Rpcs = DrotRpcInterface
    
    stat = Stat.prop('stat')    
    cfg  = Cfg.prop('cfg')
    rpc  = Rpcs.prop('rpcs')
    
    def init(self):
        # fix a feature unsude the FB_MA, the RPC_Init return silently zero even if the
        # device is not in the right state
        # TODO remove the patch when this is fixed from ESO side 
        if self.stat.substate.get() != self.SUBSTATE.NOTOP_NOTREADY:
            raise RuntimeError("Should be in NOTOP_NOTREADY state")
        self.rpc.rpcInit.rcall()
        return self.stat.is_ready
    
    def start_track(self, mode, angle=0.0) -> EltDevice.Node:
        """ Start drot tracking 
        
        Args:
            mode (int, str): tracking mode. Int constant defined in Drot.MODE.SKY, Drot.MODE.ELEV
                             str 'SKY' or 'ELEV' is also accepted
            angle (float): paSky or paPupil depending of the mode
        
        Returns:
            is_tracking:  the :class:`NodeAlias` .stat.is_tracking to check if the device is in tracking  
        """
        self.rpc.rpcStartTrack.rcall(mode, angle)
        return self.stat.is_tracking
    
    def move_angle(self, angle=0.0) -> EltDevice.Node:
        """ Move drot to angle in STAT mode 
        
        Args:
            angle (float, optional): target angle default = 0.0 
            
        Returns:
            is_standstill:  the :class:`NodeAlias` .stat.is_standstill to check if the device is 
                            in standstill. (e.i. movement finished)
        
        Example:
        
            ::
            
                wait( drot.move_angle( 34.3 ) )
        """
        self.rpc.rpcMoveAngle.rcall(angle)
        return self.stat.is_standstill
        
    def move_abs(self, pos, vel=None) -> EltDevice.Node:
        """ Move the drot to an absolute position in ENG mode 
        
        Args:
            pos (float): absolute position
            vel (float): target velocity for the movement
            
        Returns:
            is_standstill:  the :class:`NodeAlias` .stat.is_standstill to check if the device is 
                            standstill (e.i. movement finished)
        
        Example:
        
            ::
            
                wait( drot.move_abs( 34.5, 4.0 ) )
        """
        vel = self.velocity if vel is None else vel
        self.rpc.rpcMoveAbs.rcall(pos, vel)
        return self.stat.is_standstill
        
    def move_rel(self, pos, vel=None) -> EltDevice.Node:
        """ Move the drot to a relative position in ENG mode 
        
        Args:
            pos (float): relative position
            vel (float): target velocity for the movement
            
        Returns:
            is_standstill:  the :class:`NodeAlias` .stat.is_standstill to check if the device is in standstill
        
        Example:
        
            ::
            
                wait( drot.move_rel( 8.5, 4.0 ) )
        """
        vel = self.velocity if vel is None else vel
        self.rpc.rpcMoveRel.rcall(pos, vel)
        return self.stat.is_standstill
        
    def move_vel(self, vel) -> EltDevice.Node:
        """ move drot in velocity 
        
        Args:
           vel (float): target velocity
        
        Return: 
            None
        """
        self.rpc.rpcMoveVel.rcall( vel)
    
    def stop(self) -> None:
        """ Stop derotator motion 
        
        Returns:
           None
        """
        self.rpc.rpcStop.rcall()



