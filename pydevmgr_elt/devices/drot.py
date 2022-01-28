from pydevmgr_core import buildproperty, NodeVar, record_class
from pydevmgr_ua import Int16, Int32
from ..base.tools import enum_group, enum_txt, EnumTool
from ..base.eltdevice import EltDevice, GROUP

from enum import Enum

from . import trk
from .motor import Motor

from pydantic import Field 


class DrotConfig(Motor.Config):
    type: str = "Drot"

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



#  ____        _          __  __           _      _ 
# |  _ \  __ _| |_ __ _  |  \/  | ___   __| | ___| |
# | | | |/ _` | __/ _` | | |\/| |/ _ \ / _` |/ _ \ |
# | |_| | (_| | || (_| | | |  | | (_) | (_| |  __/ |
# |____/ \__,_|\__\__,_| |_|  |_|\___/ \__,_|\___|_|
# 

class DrotCfgData(Motor.Data.CfgData):
    #Drot specific parameters
    focus_sign:       NodeVar[int] = Field(-1 , description="Sign for the instrument focus Nasmyth A -> -1 cfg.nFocusSign")
    dir_sign:         NodeVar[int] = Field(1  , description="Rotator Direction sign cfg.nDirSign")
    stat_ref:         NodeVar[float] = Field(0.0, description="STAT mode reference position [UU] cfg.lrStatRef")
    sky_ref:          NodeVar[float] = Field(0.0, description="SKY mode  reference position [UU] cfg.lrSkyRef")
    elev_ref:         NodeVar[float] = Field(0.0, description="ELEV mode reference position [UU] cfg.lrElevRef")
    user_ref:         NodeVar[float] = Field(0.0, description="USER mode reference position [UU] cfg.lrUserRef")
    user_par1:        NodeVar[float] = Field(0.0, description="User Parameter, slot 1, cfg.lrUserPar1")
    user_par2:        NodeVar[float] = Field(0.0, description="User Parameter, slot 2, cfg.lrUserPar2")
    user_par3:        NodeVar[float] = Field(0.0, description="User Parameter, slot 3, cfg.lrUserPar3")
    user_par4:        NodeVar[float] = Field(0.0, description="User Parameter, slot 4, cfg.lrUserPar4")
    latitude:         NodeVar[float] = Field(-0.429833092  , description="cfg.site.latitude")
    longitude:        NodeVar[float] = Field(1.228800386   , description="cfg.site.longitude")
    trk_period:       NodeVar[int]   = Field(0  , description="cfg.nMinSkipCycles")
    trk_threshold:    NodeVar[float] = Field(1.0, description="If maximum Error is <... traking is True [UU] cfg.lrTrkThreshold cfg.lrTrkThreshold")
    
class DrotStatData(Motor.Data.StatData, trk.TrkStatData):
    alpha: NodeVar[float] = Field(0.0, description="Apparent alpha coordinate stat.apparent.alpha")
    delta: NodeVar[float] = Field(0.0, description="Apparent delta coordinate stat.apparent.delta")
    angle_on_sky: NodeVar[float] = Field(0.0, description="Angle on sky one in SKY or ELEV mode [UU]")
    
class DrotData(EltDevice.Data):    
    StatData = DrotStatData
    CfgData = DrotCfgData
    
    cfg: CfgData = CfgData()
    stat: StatData = StatData()    


#  _       _             __                
# (_)_ __ | |_ ___ _ __ / _| __ _  ___ ___ 
# | | '_ \| __/ _ \ '__| |_ / _` |/ __/ _ \
# | | | | | ||  __/ |  |  _| (_| | (_|  __/
# |_|_| |_|\__\___|_|  |_|  \__,_|\___\___|
@record_class
class DrotStatInterface(trk.TrkStatInterface):
    
    class Config(trk.TrkStatInterface.Config):
        type: str = 'Drot.Stat'
    
    Data = DrotStatData    
    ERROR = ERROR
    MODE = MODE
    SUBSTATE = SUBSTATE    

@record_class    
@buildproperty(EltDevice.Node.prop, 'parser')    
class DrotCfgInterface(Motor.CfgInterface):
    
    class Config(Motor.CfgInterface.Config):
        type: str = 'Drot.Cfg'
    
    Data = DrotCfgData
    # ################
    focus_sign : Int32
    dir_sign   : Int32
    trk_period : Int32

@record_class
@buildproperty(EltDevice.Rpc.prop, 'args_parser')
class DrotRpcInterface(EltDevice.RpcInterface):
    
    class Config(EltDevice.RpcInterface.Config):
        type: str = 'Drot.Rpc'
        
    RPC_ERROR = RPC_ERROR
    ##
    # the type of rpcMethod argument can be defined by annotation
    # All method args types must be defined in a tuple
    rpcMoveAbs    : (float, float)
    rpcMoveRel    : (float, float)
    rpcMoveAngle  : (float,)
    rpcMoveVel    : (float,)
    rpcStartTrack : (mode_parser, float)
    
#      _            _          
#   __| | _____   _(_) ___ ___ 
#  / _` |/ _ \ \ / / |/ __/ _ \
# | (_| |  __/\ V /| | (_|  __/
#  \__,_|\___| \_/ |_|\___\___|
#
@record_class
class Drot(Motor, trk.Trk):
    SUBSTATE = SUBSTATE
    MODE = MODE 
    ERROR = ERROR
    
    Config = DrotConfig
    Data = DrotData
    
    StatInterface = DrotStatInterface
    CfgInterface = DrotCfgInterface
    RpcInterface = DrotRpcInterface
    
    stat = StatInterface.prop('stat')    
    cfg  = CfgInterface.prop('cfg')
    rpc  = RpcInterface.prop('rpc')
    
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



