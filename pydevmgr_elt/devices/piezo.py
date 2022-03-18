from pydevmgr_core import NodeAlias, NodeVar, record_class
from pydevmgr_ua import Int16, Int32
from ..base.eltdevice import EltDevice, GROUP
from ..base.tools import _inc, enum_group, enum_txt, EnumTool

from pydantic import Field
from enum import Enum
from ._piezo_autobuilt import _Piezo 

#                      _              _   
#   ___ ___  _ __  ___| |_ __ _ _ __ | |_ 
#  / __/ _ \| '_ \/ __| __/ _` | '_ \| __|
# | (_| (_) | | | \__ \ || (_| | | | | |_ 
#  \___\___/|_| |_|___/\__\__,_|_| |_|\__|
# 

##### ############
# SUBSTATE
class SUBSTATE(EnumTool, int, Enum):
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
class ERROR(EnumTool, int, Enum):
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

### ##############
# RPC error
class RPC_ERROR(EnumTool, int, Enum):
    OK			                =  0
    NOT_OP                      = -1
    NOT_NOTOP_READY		        = -2
    NOT_NOTOP_NOTREADY          = -3
    MOVING_USER                 = -5
    MOVING_BIT                  = -6
    LOCAL                       = -7
    
    UNREGISTERED = -9999

# Add text definition to each constants, the definition is then accessible throught .txt attribute 
enum_txt ({
    RPC_ERROR.OK:						 'OK',
    RPC_ERROR.NOT_OP:					 'Cannot control device. Not in OP state.',
    RPC_ERROR.NOT_NOTOP_READY:		     'Call failed. Not in NOTOP_READY.',
    RPC_ERROR.NOT_NOTOP_NOTREADY:		 'Call failed. Not in NOTOP_NOTREADY/ERROR.',
    RPC_ERROR.LOCAL:					 'RPC calls not allowed in Local mode.',
    RPC_ERROR.MOVING_USER:			     'Set user value out of range.',
    RPC_ERROR.MOVING_BIT:				 'Set bit value out of range.',
    
    RPC_ERROR.UNREGISTERED:          'Unregistered RPC Error',
    })




#  _       _             __                
# (_)_ __ | |_ ___ _ __ / _| __ _  ___ ___ 
# | | '_ \| __/ _ \ '__| |_ / _` |/ __/ _ \
# | | | | | ||  __/ |  |  _| (_| | (_|  __/
# |_|_| |_|\__\___|_|  |_|  \__,_|\___\___|
class PiezoStatInterface(_Piezo.Stat):
    
    
    ERROR = ERROR
    SUBSTATE = SUBSTATE
    
    @NodeAlias.prop("is_auto", ["substate"])
    def is_auto(self, substate: int) -> bool:
        """ -> True is axis is in auto mode """
        return substate == self.SUBSTATE.OP_AUTO
    
    @NodeAlias.prop("is_pos", ["substate"])
    def is_pos(self, substate: int) -> bool:
        """ -> True is axis is in pos mode """
        return substate == self.SUBSTATE.OP_POS


    


#      _            _          
#   __| | _____   _(_) ___ ___ 
#  / _` |/ _ \ \ / / |/ __/ _ \
# | (_| |  __/\ V /| | (_|  __/
#  \__,_|\___| \_/ |_|\___\___|
#
@record_class
class Piezo(_Piezo):
    SUBSTATE = SUBSTATE
    ERROR = ERROR
    
    
    Stat = PiezoStatInterface
    
    stat = Stat.prop('stat')    
         
    def auto(self) -> None:
        """ turn on auto mode 
        
        Returns:
           None
        """
        self.rpc.rpcAuto.rcall()   
    
    def pos(self):
        """ turn to POS mode 
        
        Returns:
           None
        """
        self.rpc.rpcPos.rcall()
    
    def home(self) -> None:
        """ send  piezos home 
        
        Returns:
           None
        """
        self.rpc.rpcHome.rcall()
    
    def move_bits(self, pos1=0, pos2=0, pos3=0) -> None:
        """ move piezos to bits position 
        
        Args:
            pos1 (int): piezo 1 position (bits)
            pos2 (int): piezo 2 position (bits) 
            pos3 (int): piezo 3 position (bits)
        """
        # pos1, pos2, pos3 are piezo set positions in bits - integers.
        self.rpc.rpcMoveBits.rcall(pos1, pos2, pos3)
    
    def move_user(self, pos1=0.0, pos2=0.0, pos3=0.0) -> None:
        """ move piezos to user  position 
        
        Args:
            pos1 (float): piezo 1 position (user)
            pos2 (float): piezo 2 position (user) 
            pos3 (float): piezo 3 position (user)
        """
        # pos1, pos2, pos3 are piezo set positions in UU - float.
        self.rpc.rpcMoveUser.rcall(pos1, pos2, pos3)
    
    def stop(self) -> None:
        """ stop movement """
        self.rpc.rpcStop.rcall()


