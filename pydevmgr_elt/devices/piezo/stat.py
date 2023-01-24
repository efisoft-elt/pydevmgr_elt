
from pydevmgr_core import   NodeVar
from pydevmgr_core.base.dataclass import set_data_model
from pydevmgr_core.decorators  import nodealias 

from pydevmgr_elt.base import EltDevice,  GROUP
from pydevmgr_elt.base.tools import _inc, enum_group, enum_txt
from typing import Any
from enum import Enum

Base = EltDevice.Stat

N = Base.Node # Base Node
NC = N.Config
NV = NodeVar # used in Data 
#                      _              _   
#   ___ ___  _ __  ___| |_ __ _ _ __ | |_ 
#  / __/ _ \| '_ \/ __| __/ _` | '_ \| __|
# | (_| (_) | | | \__ \ || (_| | | | | |_ 
#  \___\___/|_| |_|___/\__\__,_|_| |_|\__|
# 


##### ############
# SUBSTATE
class SUBSTATE(int, Enum):
    NONE                  =   0
    NOTOP_NOTREADY		  = 100
    NOTOP_READY		      = 101
    NOTOP_INITIALISING	  = 102
    NOTOP_ERROR			  = 199
    OP_DISABLING		  = 205
    OP_POS                = 203
    OP_AUTO               = 204
    OP_ERROR			  = 299
    
    UNREGISTERED = -9999
    
enum_group ( {
    SUBSTATE.NONE                   : GROUP.UNKNOWN,
    SUBSTATE.NOTOP_NOTREADY         : GROUP.NOK,
    SUBSTATE.NOTOP_READY            : GROUP.NOK,
    SUBSTATE.NOTOP_INITIALISING     : GROUP.BUZY,
    SUBSTATE.NOTOP_ERROR            : GROUP.ERROR, 
    SUBSTATE.OP_DISABLING		   : GROUP.BUZY,
    SUBSTATE.OP_POS                 : GROUP.OK, 
    SUBSTATE.OP_AUTO                : GROUP.OK, 
    SUBSTATE.OP_ERROR               : GROUP.ERROR, 
})

### ##############
# ERROR
class ERROR(int, Enum):
    OK		      = 0
    HW_NOT_OP     = 1			
    ON_FAILURE    = 2
    MAXON         = 3
    OUT_OF_RANGE  = 4
    USER2BIT_ZERO = 5
	
	# Simulator errors
    NOT_INITIALISED		= 90
    ZERO_POINTER		= 100	
    
    UNREGISTERED = -9999

# Add text definition to each constants, the definition is then accessible throught .txt attribute     
enum_txt ({
    ERROR.OK:				 'OK',
    ERROR.HW_NOT_OP:		 'ERROR: TwinCAT not in OP state or CouplerState not mapped.',
    ERROR.ON_FAILURE:        'ERROR: Piezo HW failure',
    ERROR.MAXON:             'ERROR: Maximum ON time exceeded.',
    ERROR.OUT_OF_RANGE:      'ERROR: Piezo set position out of range',
    ERROR.USER2BIT_ZERO:     'ERROR: cfg.lrUser2Bit has zero value.',
    
    ERROR.UNREGISTERED:       'ERROR: Unregistered Error'
})




    #  ____  _        _     ___       _             __                 
    # / ___|| |_ __ _| |_  |_ _|_ __ | |_ ___ _ __ / _| __ _  ___ ___  
    # \___ \| __/ _` | __|  | || '_ \| __/ _ \ '__| |_ / _` |/ __/ _ \ 
    #  ___) | || (_| | |_   | || | | | ||  __/ |  |  _| (_| | (_|  __/ 
    # |____/ \__\__,_|\__| |___|_| |_|\__\___|_|  |_|  \__,_|\___\___| 
@set_data_model
class PiezoStat(Base):
    # Add the constants to this class 
    ERROR = ERROR
    SUBSTATE = SUBSTATE
    
    class Config(Base.Config):
        # define all the default configuration for each nodes. 
        # e.g. the suffix can be overwriten in construction (from a map file for instance)
        # all configured node will be accessible by the Interface
        actual_pos_bit1: NC = NC(suffix='stat.nActPosBit[0].nValue' , vtype=int)
        actual_pos_bit2: NC = NC(suffix='stat.nActPosBit[1].nValue' , vtype=int)
        actual_pos_bit3: NC = NC(suffix='stat.nActPosBit[2].nValue' , vtype=int)
        actual_pos_user1: NC = NC(suffix='stat.lrActPosUsr[0].lrValue' , vtype=float)
        actual_pos_user2: NC = NC(suffix='stat.lrActPosUsr[1].lrValue' , vtype=float)
        actual_pos_user3: NC = NC(suffix='stat.lrActPosUsr[2].lrValue' , vtype=float)
        error_code: NC = NC(suffix='stat.nErrorCode', vtype=int )
        local: NC = NC(suffix='stat.bLocal', vtype=bool )
        mon_act_pos_bit1: NC = NC(suffix='stat.monSetPosBit_0', vtype=int )
        mon_act_pos_bit2: NC = NC(suffix='stat.monSetPosBit_1', vtype=int )
        mon_act_pos_bit3: NC = NC(suffix='stat.monSetPosBit_2', vtype=int )
        mon_act_pos_usr1: NC = NC(suffix='stat.monActPosUsr_0', vtype=float )
        mon_act_pos_usr2: NC = NC(suffix='stat.monActPosUsr_1', vtype=float )
        mon_act_pos_usr3: NC = NC(suffix='stat.monActPosUsr_2', vtype=float )
        state: NC = NC(suffix='stat.nState', vtype=int )
        substate: NC = NC(suffix='stat.nSubstate', vtype=int )

    
    @nodealias("substate")
    def is_auto(self, substate: int) -> bool:
        """ -> True is axis is in auto mode """
        return substate == self.SUBSTATE.OP_AUTO
    
    @nodealias("substate")
    def is_pos(self, substate: int) -> bool:
        """ -> True is axis is in pos mode """
        return substate == self.SUBSTATE.OP_POS


if __name__ == "__main__":
    PiezoStat( )
