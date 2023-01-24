
import weakref
from pydevmgr_core import   NodeVar, set_data_model
from pydevmgr_core.base.base import ParentWeakRef
from pydevmgr_core.decorators import nodealias 

from pydevmgr_elt.base import EltDevice,  GROUP
from pydevmgr_elt.base.tools import _inc, enum_group, enum_txt
from pydevmgr_elt.devices.motor.positions import PositionConfig 
from typing import Optional, List
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
    NONE =  0

    NOTOP_NOTREADY =  100
    NOTOP_READY = 101
    NOTOP_INITIALIZING = 102
    NOTOP_ABORTING = 107
    NOTOP_CLEARING_NOVRAM = 108

    NOTOP_ERROR =  199

    OP_STANDSTILL =216
    OP_MOVING = 217
    OP_SETTING_POS = 218
    OP_STOPPING = 219

    OP_ERROR =299
    
    UNREGISTERED = -9999

# Add text definition to each constants, the definition is then accessible throught .txt attribute 
enum_group({
    SUBSTATE.NONE                   : GROUP.UNKNOWN,
    SUBSTATE.NOTOP_NOTREADY         : GROUP.NOK,
    SUBSTATE.NOTOP_READY            : GROUP.NOK,
    SUBSTATE.NOTOP_INITIALIZING     : GROUP.BUZY,
    SUBSTATE.NOTOP_ABORTING         : GROUP.BUZY,
    SUBSTATE.NOTOP_CLEARING_NOVRAM  : GROUP.BUZY,
    SUBSTATE.NOTOP_ERROR            : GROUP.ERROR, 
    SUBSTATE.OP_STANDSTILL          : GROUP.OK, 
    SUBSTATE.OP_MOVING              : GROUP.BUZY, 
    SUBSTATE.OP_SETTING_POS         : GROUP.BUZY,
    SUBSTATE.OP_STOPPING            : GROUP.BUZY,
    SUBSTATE.OP_ERROR               : GROUP.ERROR,    
})


class ERROR(int,  Enum):
    OK				      = _inc(0) # init the inc to zero
    HW_NOT_OP              = _inc()
    LOCAL                  = _inc()
    INIT_ABORTED           = _inc()
    TIMEOUT_INIT           = _inc()
    TIMEOUT_MOVE           = _inc()
    TIMEOUT_RESET          = _inc()
    TIMEOUT_SETPOS         = _inc()
    TIMEOUT_USER_PREINIT   = _inc()
    TIMEOUT_USER_POSTINIT  = _inc()
    TIMEOUT_USER_PREMOVE   = _inc()
    TIMEOUT_USER_POSTMOVE  = _inc()
    SETPOS                 = _inc()
    STOP                   = _inc()
    ABORT                  = _inc()
    SW_LIMIT_LOWER         = _inc()
    SW_LIMIT_UPPER         = _inc()
    BRAKE_ACTIVE           = _inc()
    BRAKE_ENGAGE           = _inc()
    BRAKE_DISENGAGE        = _inc()
    SWITCH_NOT_USED        = _inc()
    ENABLE                 = _inc()
    NOVRAM_READ            = _inc()
    NOVRAM_WRITE           = _inc()
    SWITCH_EXIT            = _inc()
    STOP_LIMITS_BOTH       = _inc()
    HW_LIMITS_BOTH         = _inc()
    IN_POS                 = _inc()
    LOCKED                 = _inc()
    SoE_ADS_ERROR          = _inc()
    SoE_SERCOS_ERROR       = _inc()

    # Simulator errors
    SIM_NOT_INITIALISED			= 90
    SIM_NULL_POINTER			= 100	

    # TwinCAT errors
    TC_VEL						= 16929	
    TC_NOT_READY_FOR_START		= 16933	
    TC_DISABLED_MOVE			= 16992	
    TC_BISECTION				= 17022	
    TC_MODULO_POS				= 17026	
    TC_STOP_ACTIVE				= 17135	
    TC_VEL_NEG					= 17241	
    TC_TARGET_LSW				= 17504	
    TC_TARGET_USW				= 17505	
    TC_FOLLOWING_ERROR			= 17744	
    TC_NOT_READY				= 18000	
    TC_IN_POS_6_SEC				= 19207	

    UNREGISTERED = -9999

# Add text definition to each constants, the definition is then accessible throught .txt attribute     
enum_txt ({
    ERROR.OK:				   'OK',
    ERROR.HW_NOT_OP:			 'ERROR: TwinCAT not OP or CouplerState not mapped.',
    ERROR.LOCAL:				 'ERROR: Control not allowed. Motor in Local mode.',
    ERROR.INIT_ABORTED:		     'ERROR: INIT command aborted.',
    ERROR.TIMEOUT_INIT:		     'ERROR: INIT timed out.',
    ERROR.TIMEOUT_MOVE:		     'ERROR: Move timed out.',
    ERROR.TIMEOUT_RESET:		 'ERROR: Reset timed out.',
    ERROR.TIMEOUT_SETPOS:		 'ERROR: Set Position timed out.',
    ERROR.TIMEOUT_USER_PREINIT:  'ERROR: User PRE-INIT timed out.',
    ERROR.TIMEOUT_USER_POSTINIT: 'ERROR: User POST-INIT timed out.',
    ERROR.TIMEOUT_USER_PREMOVE:  'ERROR: User PRE-MOVE timed out.',
    ERROR.TIMEOUT_USER_POSTMOVE: 'ERROR: User POST-MOVE timed out.',
    ERROR.SETPOS:				 'ERROR: Set Position failed.',
    ERROR.STOP:				     'ERROR: STOP failed.',
    
    ERROR.ABORT:			  'ERROR: Motion aborted.',
    ERROR.SW_LIMIT_LOWER:	  'ERROR: Lower SW Limit Exceeded.',
    ERROR.SW_LIMIT_UPPER:	  'ERROR: Upper SW Limit Exceeded.',
    ERROR.BRAKE_ACTIVE:		  'ERROR: Cannot move. Brake active.',
    ERROR.BRAKE_ENGAGE:		  'ERROR: Failed to engage brake.',
    ERROR.BRAKE_DISENGAGE:	  'ERROR: Failed to disengage brake.',
    ERROR.SWITCH_NOT_USED:	  'ERROR: Switch was not detected in previous INIT action.',
    ERROR.ENABLE:			  'ERROR: Failed to enable Axis.',
    ERROR.NOVRAM_READ:		  'ERROR: Failed to read from NOVRAM',
    ERROR.NOVRAM_WRITE:		  'ERROR: Failed to write to NOVRAM',
    ERROR.SWITCH_EXIT:		  'ERROR: Timeout on switch exit. Check nTimeoutSwitch.',
    ERROR.STOP_LIMITS_BOTH:	  'ERROR: Both LSTOP and USTOP limits active.',
    ERROR.HW_LIMITS_BOTH:	  'ERROR: Both limit switches LHW and UHW active.',
    ERROR.IN_POS:			  'ERROR: In-Pos switch not active at the end of movement.',
    ERROR.LOCKED:			  'ERROR: Motor Locked! Cannot move.',
    ERROR.SoE_ADS_ERROR:	  'ERROR: SoE ADS Error.',
    ERROR.SoE_SERCOS_ERROR:	  'ERROR: SoE Sercos Error.',

    ERROR.SIM_NOT_INITIALISED:  'ERROR: Simulator not initialised.',
    ERROR.SIM_NULL_POINTER:	    'ERROR: Simulator input parameter is a NULL pointer.',
    
    # Beckhoff TwinCAT most common errors
    ERROR.TC_VEL:				    'ERROR: Requested set velocity is not allowed.',
    ERROR.TC_NOT_READY_FOR_START:   'ERROR: Drive not ready during axis start. Maybe SW limits.',
    ERROR.TC_DISABLED_MOVE:		    'ERROR: Motor disabled while moving. Reset required!',
    ERROR.TC_BISECTION:			    'WARNING: Motion command could not be realized (BISECTION)',
    ERROR.TC_MODULO_POS:		    'ERROR: Target position >= full turn (modulo-period)',
    ERROR.TC_STOP_ACTIVE:		    'ERROR: Stop command still active. Axis locked. Reset required!',
    ERROR.TC_VEL_NEG:			    'ERROR: Set velocity not allowed (<=0)',
    ERROR.TC_TARGET_LSW:		    'ERROR: Target position beyond Lower Software Limit.',
    ERROR.TC_TARGET_USW:		    'ERROR: Target position beyond Upper Software Limit.',
    ERROR.TC_FOLLOWING_ERROR:	    'ERROR: Following error. Reset required!',
    ERROR.TC_NOT_READY:		        'ERROR: Drive not ready for operation.',
    ERROR.TC_IN_POS_6_SEC:	        'ERROR: In-position 6 sec timeout. Reset required!',
    
    ERROR.UNREGISTERED:        'ERROR: Unregistered Error'
})



    #  ____  _        _     ___       _             __                 
    # / ___|| |_ __ _| |_  |_ _|_ __ | |_ ___ _ __ / _| __ _  ___ ___  
    # \___ \| __/ _` | __|  | || '_ \| __/ _ \ '__| |_ / _` |/ __/ _ \ 
    #  ___) | || (_| | |_   | || | | | ||  __/ |  |  _| (_| | (_|  __/ 
    # |____/ \__\__,_|\__| |___|_| |_|\__\___|_|  |_|  \__,_|\___\___| 

@set_data_model
class MotorStat(ParentWeakRef, Base):
    # Add the constants to this class 
    ERROR = ERROR
    SUBSTATE = SUBSTATE
    


    class Config(Base.Config):
        # define all the default configuration for each nodes. 
        # e.g. the suffix can be overwriten in construction (from a map file for instance)
        # all configured node will be accessible by the Interface
        axis_brake:       NC  =  NC(suffix='stat.bBrakeActive',        vtype=bool   )
        axis_enable:      NC  =  NC(suffix='stat.bEnabled',            vtype=bool   )
        axis_info_data1:  NC  =  NC(suffix='stat.nInfoData1',          vtype=int    )
        axis_info_data2:  NC  =  NC(suffix='stat.nInfoData2',          vtype=int    )
        axis_inposition:  NC  =  NC(suffix='stat.bInPosition',         vtype=bool   )
        axis_lock:        NC  =  NC(suffix='stat.bLock',               vtype=bool   )
        axis_ready:       NC  =  NC(suffix='stat.bAxisReady',          vtype=bool   )
        backlash_step:    NC  =  NC(suffix='stat.nBacklashStep',       vtype=int    )
        error_code:       NC  =  NC(suffix='stat.nErrorCode',          vtype=int    )
        init_action:      NC  =  NC(suffix='stat.nInitAction',         vtype=int    )
        init_step:        NC  =  NC(suffix='stat.nInitStep',           vtype=int    )
        initialised:      NC  =  NC(suffix='stat.bInitialised',        vtype=bool   )
        local:            NC  =  NC(suffix='stat.bLocal',              vtype=bool   )
        mode:             NC  =  NC(suffix='stat.nMode',               vtype=int    )
        pos_actual:       NC  =  NC(suffix='stat.lrPosActual',         vtype=float  )
        pos_error:        NC  =  NC(suffix='stat.lrPosError',          vtype=float  )
        pos_target:       NC  =  NC(suffix='stat.lrPosTarget',         vtype=float  )
        scale_factor:     NC  =  NC(suffix='stat.lrScaleFactor',       vtype=float  )
        signal_index:     NC  =  NC(suffix='stat.signals[3].bActive',  vtype=bool   )
        signal_lhw:       NC  =  NC(suffix='stat.signals[1].bActive',  vtype=bool   )
        signal_lstop:     NC  =  NC(suffix='stat.signals[0].bActive',  vtype=bool   )
        signal_ref:       NC  =  NC(suffix='stat.signals[2].bActive',  vtype=bool   )
        signal_uhw:       NC  =  NC(suffix='stat.signals[4].bActive',  vtype=bool   )
        signal_ustop:     NC  =  NC(suffix='stat.signals[5].bActive',  vtype=bool   )
        state:            NC  =  NC(suffix='stat.nState',              vtype=int    )
        status:           NC  =  NC(suffix='stat.nStatus',             vtype=int    )
        substate:         NC  =  NC(suffix='stat.nSubstate',           vtype=int    )
        vel_actual:       NC  =  NC(suffix='stat.lrVelActual',         vtype=float  )
    # for this one we redefine the init so it does accept a mot_positions argument
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.positions = []
        self.tolerance = 1.0
    
        
    @nodealias("substate")
    def is_moving(self, substate)-> bool:
        """ -> True is axis is moving """
        return substate == self.SUBSTATE.OP_MOVING

    @nodealias("substate")
    def is_standstill(self,  substate)-> bool:
        """ -> True is axis is standstill """
        return substate == self.SUBSTATE.OP_STANDSTILL
    
    
    @nodealias("pos_actual")
    def pos_name(self, pos_actual)-> float:
        parent = self.get_parent()
        if not parent: return ''
        try:
            positions = parent.config.positions
        except AttributeError:
            return '' 
        tol = parent.config.tolerance 
        if not positions: return ''
        for pos in positions:
            if abs( pos.value-pos_actual)<tol:
                return pos.name
        return ''
  
  
if __name__ == "__main__":
    MotorStat( local=NC(parser=float) )
    print("OK")
