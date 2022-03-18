from pydevmgr_core import NodeAlias,  NodeVar, record_class
from pydevmgr_ua import Int32, UInt32
from ..base.eltdevice import EltDevice, GROUP

from ..base.tools import  _inc, enum_group, enum_txt, EnumTool
from enum import Enum
from typing import Optional

from ._lamp_autobuilt import _Lamp

class LampCtrlConfig(EltDevice.Config.CtrlConfig):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    low_fault:        Optional[bool] = False   # If T, signal is active low
    low_on:           Optional[bool] = False   # If T, signal is active low
    low_switch:       Optional[bool] = False   # If T, signal is active low
    initial_state:    Optional[bool] = False
    timeout:          Optional[int]  = 2000 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
class LampConfig(_Lamp.Config):
    CtrlConfig = LampCtrlConfig
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    type: str = "Lamp"
    ctrl_config : CtrlConfig = CtrlConfig() 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
#                      _              _   
#   ___ ___  _ __  ___| |_ __ _ _ __ | |_ 
#  / __/ _ \| '_ \/ __| __/ _` | '_ \| __|
# | (_| (_) | | | \__ \ || (_| | | | | |_ 
#  \___\___/|_| |_|___/\__\__,_|_| |_|\__|
# 
##### ###########
# SUBSTATE
class SUBSTATE(EnumTool, int, Enum):
    NONE                  =   0    
    NOTOP_NOTREADY        = 100    
    NOTOP_INITIALISING    = 102    
    NOTOP_READY_OFF       = 103    
    NOTOP_READY_ON        = 104    
    NOTOP_ERROR           = 199    
    OP_DISABLING          = 205    
    OP_OFF                = 206    
    OP_SWITCHING_OFF      = 207    
    OP_COOLING            = 208    
    OP_ON                 = 209    
    OP_SWITCHING_ON       = 210    
    OP_WARMING            = 211    
    OP_ERROR              = 299
    
    UNREGISTERED = -9999
enum_group( {
        SUBSTATE.NONE                   : GROUP.UNKNOWN,
        SUBSTATE.NOTOP_NOTREADY         : GROUP.NOK,
        SUBSTATE.NOTOP_READY_OFF        : GROUP.NOK,
        SUBSTATE.NOTOP_READY_ON         : GROUP.NOK,
        SUBSTATE.NOTOP_INITIALISING     : GROUP.BUZY,
        SUBSTATE.NOTOP_ERROR            : GROUP.ERROR, 
  
        SUBSTATE.OP_DISABLING            : GROUP.BUZY, 
        SUBSTATE.OP_SWITCHING_OFF        : GROUP.BUZY,
        SUBSTATE.OP_SWITCHING_ON         : GROUP.BUZY,

        SUBSTATE.OP_COOLING              : GROUP.BUZY,
        SUBSTATE.OP_WARMING              : GROUP.BUZY,
        SUBSTATE.OP_ON                   : GROUP.OK,
        SUBSTATE.OP_OFF                  : GROUP.OK,
        SUBSTATE.OP_ERROR                : GROUP.ERROR,    
    })


### #############
# ERROR
class ERROR(EnumTool, int, Enum):
    OK					= _inc(0)
    HW_NOT_OP           = _inc()
    INIT_FAILURE        = _inc()		
    UNEXPECTED_OFF      = _inc()
    UNEXPECTED_ON       = _inc()
    FAULT_SIG           = _inc()
    MAXON               = _inc()
    STILL_COOLING       = _inc()
    TIMEOUT_DISABLE     = _inc()
    TIMEOUT_INIT        = _inc()
    TIMEOUT_OFF         = _inc()
    TIMEOUT_ON          = _inc()
    # Simulator errors
    SIM_NOT_INITIALISED	= 90
    SIM_NULL_POINTER    = 100	
    
    UNREGISTERED = -9999
enum_txt ({
    ERROR.OK:					 'OK',
	ERROR.HW_NOT_OP:			 'ERROR: TwinCAT not in OP state or CouplerState not mapped.',
    ERROR.INIT_FAILURE:		     'ERROR: INIT command aborted due to STOP or RESET.',
	ERROR.UNEXPECTED_OFF:		 'ERROR: Lamp unexpectedly switched OFF.',
	ERROR.UNEXPECTED_ON:		 'ERROR: Lamp unexpectedly switched ON.',
	ERROR.FAULT_SIG:			 'ERROR: Fault signal active.',
	ERROR.MAXON:				 'ERROR: Lamp maximum ON time exceeded.',
	ERROR.STILL_COOLING:		 'ERROR: ON command not allowed while cooling.',
	ERROR.TIMEOUT_DISABLE:	     'ERROR: Disable timed out.',
	ERROR.TIMEOUT_INIT:		     'ERROR: Init timed out.',
	ERROR.TIMEOUT_OFF:		     'ERROR: Switching OFF timed out.',
	ERROR.TIMEOUT_ON:			 'ERROR: Switching ON timed out.',
	ERROR.SIM_NOT_INITIALISED:   'ERROR: Lamp simulator not initialised.',
	ERROR.SIM_NULL_POINTER:	     'ERROR: NULL pointer to Lamp.',
    ERROR.UNREGISTERED:          'ERROR: Unregistered Error'
    })

### #############
#
# RPC error
class RPC_ERROR(EnumTool, int, Enum):    
    OK                 =  0     
    NOT_OP             = -1    
    NOT_NOTOP_READY    = -2    
    NOT_NOTOP_NOTREADY = -3    
    SWITCHING_ON       = -4    
    SWITCHING_OFF      = -5    
    COOLING            = -6    
    LOCAL              = -7
    
    UNREGISTERED = -9999
enum_txt ( {
    RPC_ERROR.OK:						 'OK',
	RPC_ERROR.NOT_OP:					 'Cannot control lamp. Not in OP state.',
	RPC_ERROR.NOT_NOTOP_READY:		 'Call failed. Not in NOTOP_READY.',
	RPC_ERROR.NOT_NOTOP_NOTREADY:		 'Call failed. Not in NOTOP_NOTREADY/ERROR.',
	RPC_ERROR.SWITCHING_ON:			 'Lamp OFF failed. Still switching ON.',
	RPC_ERROR.SWITCHING_OFF:			 'Lamp ON failed. Still switching OFF.',
	RPC_ERROR.COOLING:				 'Lamp ON failed. Still cooling down.',
	RPC_ERROR.LOCAL:					 'RPC calls not allowed in Local mode',
    RPC_ERROR.UNREGISTERED:           'Unregistered RPC Error'
})




#  _       _             __                
# (_)_ __ | |_ ___ _ __ / _| __ _  ___ ___ 
# | | '_ \| __/ _ \ '__| |_ / _` |/ __/ _ \
# | | | | | ||  __/ |  |  _| (_| | (_|  __/
# |_|_| |_|\__\___|_|  |_|  \__,_|\___\___|
class LampStatInterface(_Lamp.Stat):
     
    ERROR = ERROR
    SUBSTATE = SUBSTATE
    
    @NodeAlias.prop("is_ready", "substate")
    def is_ready(self, substate):
        """ Alias node: True if lamp is ready (substate NOTOP_READY_ON or NOTOP_READY_OFF) """
        return substate in [self.SUBSTATE.NOTOP_READY_ON, self.SUBSTATE.NOTOP_READY_OFF]
    
    @NodeAlias.prop("is_off", "substate")
    def is_off(self, substate):
        """  Alias node: True if lamp is off """
        return substate == self.SUBSTATE.OP_OFF
    
    @NodeAlias.prop("is_on", "substate")
    def is_on(self, substate):
        """  Alias node: True if lamp is on """
        return substate == self.SUBSTATE.OP_ON




#      _            _          
#   __| | _____   _(_) ___ ___ 
#  / _` |/ _ \ \ / / |/ __/ _ \
# | (_| |  __/\ V /| | (_|  __/
#  \__,_|\___| \_/ |_|\___\___|
#
@record_class
class Lamp(_Lamp):    
    SUBSTATE = SUBSTATE    
    ERROR = ERROR
    Config = LampConfig
    
    Stat= LampStatInterface
    
                
    stat = Stat.prop('stat')    
    
    def switch_on(self, intensity, time_limit) -> EltDevice.Node:
 
        """ switch on the lamp 
        
        Args:
            intensity (float): in % 
            time_limit (float): number of second the lamp will stay on
        """       
        # intensity - float, onTimeLimit - integer
        
        self.rpc.rpcSwitchOn.rcall(intensity, time_limit)

        return self.stat.is_on
         
    def switch_off(self) -> EltDevice.Node:
        """ switch off the lamp """        
        self.rpc.rpcSwitchOff.rcall()
        return self.stat.is_off
    


