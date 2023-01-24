
from pydevmgr_core import   NodeVar
from pydevmgr_core.base.dataclass import set_data_model
from pydevmgr_core.decorators import nodealias 

from pydevmgr_elt.base import EltDevice,  GROUP
from pydevmgr_elt.base.tools import  enum_group, enum_txt

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



class SUBSTATE(int, Enum):

    NONE    		= 0
    
    NOTOP_NOTREADY    = 100
    NOTOP_READY		= 101
    NOTOP_ERROR		= 199
    
    OP_MONITORING	= 200
    OP_ERROR		= 299
    UNREGISTERED = -9999


# Add text definition to each constants, the definition is then accessible throught .txt attribute         

enum_group ({
        SUBSTATE.NONE                   : GROUP.UNKNOWN,
        SUBSTATE.NOTOP_NOTREADY         : GROUP.NOK,
        SUBSTATE.NOTOP_READY            : GROUP.NOK,
        SUBSTATE.NOTOP_ERROR            : GROUP.ERROR, 
  
        SUBSTATE.OP_MONITORING           : GROUP.BUZY, 
        SUBSTATE.OP_ERROR                : GROUP.ERROR,    
    })
    


class ERROR(int,  Enum):

    OK					= 0
    HW_NOT_OP			= 1			
    WRONG_CMD			= 2			
    INIT_FAILURE		= 3		

    NOT_INITIALISED		= 90
    ZERO_POINTER		= 100	# Simulator error_code
    
    UNREGISTERED = -9999

# Add text definition to each constants, the definition is then accessible throught .txt attribute     
enum_txt ({
	ERROR.OK:			'OK',
	ERROR.HW_NOT_OP:	'ERROR: HW not in OP state',
    ERROR.INIT_FAILURE: 'ERROR: INIT failed', 
    })



    #  ____  _        _     ___       _             __                 
    # / ___|| |_ __ _| |_  |_ _|_ __ | |_ ___ _ __ / _| __ _  ___ ___  
    # \___ \| __/ _` | __|  | || '_ \| __/ _ \ '__| |_ / _` |/ __/ _ \ 
    #  ___) | || (_| | |_   | || | | | ||  __/ |  |  _| (_| | (_|  __/ 
    # |____/ \__\__,_|\__| |___|_| |_|\__\___|_|  |_|  \__,_|\___\___| 

@set_data_model
class SensorStat(Base):
    # Add the constants to this class 
    ERROR = ERROR
    SUBSTATE = SUBSTATE
    
    class Config(Base.Config):
        # define all the default configuration for each nodes. 
        # e.g. the suffix can be overwriten in construction (from a map file for instance)
        # all configured node will be accessible by the Interface


        substate:       NC = NC(suffix="stat.nSubstate", vtype=(SUBSTATE, SUBSTATE.NONE), output_parser=SUBSTATE)
        local:          NC = NC(suffix="stat.bLocal", vtype=bool)
        error_code:     NC = NC(suffix="stat.nErrorCode", vtype=int)

    @nodealias("substate")
    def is_ready(self, substate) -> bool:
        """ Alias node: True if lamp is ready (substate NOTOP_READY_ON or NOTOP_READY_OFF) """
        return substate in [self.SUBSTATE.NOTOP_READY]

if __name__ == "__main__":
    SensorStat()
