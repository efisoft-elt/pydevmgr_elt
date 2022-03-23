
from pydevmgr_core import  NodeAlias1, Defaults, NodeVar
from pydevmgr_elt.base import EltInterface,  GROUP
from pydevmgr_elt.devices.motor import Motor
from pydevmgr_elt.base.tools import _inc, enum_group, enum_txt, EnumTool

from enum import Enum
Base = Motor.Stat

N = Base.Node # Base Node
NC = N.Config
ND = Defaults[NC] # this typing var says that it is a Node object holding default values 
NV = NodeVar # used in Data 
#                      _              _   
#   ___ ___  _ __  ___| |_ __ _ _ __ | |_ 
#  / __/ _ \| '_ \/ __| __/ _` | '_ \| __|
# | (_| (_) | | | \__ \ || (_| | | | | |_ 
#  \___\___/|_| |_|___/\__\__,_|_| |_|\__|
# 

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

# ERROR are iddentical then Drot no need to change



    #  ____  _        _     ___       _             __                 
    # / ___|| |_ __ _| |_  |_ _|_ __ | |_ ___ _ __ / _| __ _  ___ ___  
    # \___ \| __/ _` | __|  | || '_ \| __/ _ \ '__| |_ / _` |/ __/ _ \ 
    #  ___) | || (_| | |_   | || | | | ||  __/ |  |  _| (_| | (_|  __/ 
    # |____/ \__\__,_|\__| |___|_| |_|\__\___|_|  |_|  \__,_|\___\___| 

class DrotStat(Base):
    SUBSTATE = SUBSTATE
    MODE = MODE 
    class Config(Base.Config):
        # define all the default configuration for each nodes. 
        # e.g. the suffix can be overwriten in construction (from a map file for instance)
        # all configured node will be accessible by the Interface

        # All other nodes are similar to Drot
        state:            ND = NC (suffix="sm.nState")
        substate:         ND = NC (suffix="sm.nSubstate")
        initialised:      ND = NC (suffix="bInitialised")
        track_mode:       ND = NC (suffix="nMode")
        alpha:            ND = NC (suffix="apparent.alpha")
        delta:            ND = NC (suffix="apparent.delta")
        angle_on_sky:     ND = NC (suffix="lrAngleOnSky")
        


    # We can add some nodealias to compute some stuff on the fly 
    # If they node to be configured one can set a configuration above 
    @NodeAlias1.prop(node="track_mode")
    def track_mode_txt(self, track_mode: int) -> str:
        return self.MODE(track_mode).name
    
    @NodeAlias1.prop(node="substate")
    def is_presetting(self,  substate: int) -> bool:
        """ -> True is axis is preseting """
        return substate == self.SUBSTATE.OP_PRESETTING
    
    @NodeAlias1.prop(node="substate")
    def is_tracking(self,  substate: int) -> bool:
        """ -> True is axis is tracking """
        return substate == self.SUBSTATE.OP_TRACKING


    # Node Alias here     
    # Build the Data object to be use with DataLink, the type and default are added here 
    class Data(Base.Data):
        track_mode: NV[int] = 0
        alpha: NV[float] = 0.0
        delta: NV[float] = 0.0 
        angle_on_sky: NV[float] = 0.0 
        
if __name__ == "__main__":
    DrotStat( )
