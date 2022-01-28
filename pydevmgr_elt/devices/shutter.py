from pydevmgr_core import NodeAlias, NodeAlias1, buildproperty, NodeVar, record_class
from pydevmgr_ua import  UInt32
from ..base.eltdevice import EltDevice, GROUP
from ..base.tools import _inc, enum_group, enum_txt, EnumTool
from ..base.eltnode import EltNode

from enum import Enum
from pydantic import Field
from typing import Optional

class ShutterCtrlConfig(EltDevice.Config.CtrlConfig):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure (on top of CtrlConfig)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    low_closed:    Optional[bool] =  False
    low_fault:     Optional[bool] =  False  # If T, signal is active low
    low_open:      Optional[bool] =  False  # If T, signal is active low
    low_switch:    Optional[bool] =  False  # If T, signal is active low
    ignore_closed: Optional[bool] =  False  # If T, ignore the signal
    ignore_fault:  Optional[bool] =  False  # If T, ignore the signal
    ignore_open:   Optional[bool] =  False  # If T, ignore the signal
    initial_state: Optional[bool] =  False
    timeout:       Optional[int]  =  2000
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
class ShutterConfig(EltDevice.Config):
    CtrlConfig = ShutterCtrlConfig
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure (redefine the ctrl_config)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    type: str = "Shutter"
    ctrl_config : CtrlConfig = CtrlConfig()     
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    

#                      _              _   
#   ___ ___  _ __  ___| |_ __ _ _ __ | |_ 
#  / __/ _ \| '_ \/ __| __/ _` | '_ \| __|
# | (_| (_) | | | \__ \ || (_| | | | | |_ 
#  \___\___/|_| |_|___/\__\__,_|_| |_|\__|
# 



class SUBSTATE(EnumTool, int, Enum):
    OFF = 0
    NOT_OP = 1
    OP = 2
    NOT_OP_NOT_READY = 100
    NOT_OP_INITIALIZING = 102
    NOT_OP_READY_CLOSED = 105
    NOT_OP_READY_OPEN = 106
    NOT_OP_FAILURE = 199
    NOT_OP_ERROR = 199
    OP_DISABLING = 205
    OP_CLOSED = 212
    OP_CLOSING = 213
    OP_OPEN = 214
    OP_OPENING = 215
    OP_FAILURE = 299
    
    UNREGISTERED = -9999

# Add text definition to each constants, the definition is then accessible throught .txt attribute         
enum_group ({
        SUBSTATE.OFF                   : GROUP.UNKNOWN,
        SUBSTATE.OP                    : GROUP.OK,
        SUBSTATE.NOT_OP_NOT_READY      : GROUP.NOK,
        SUBSTATE.NOT_OP_READY_CLOSED   : GROUP.NOK,
        SUBSTATE.NOT_OP_READY_OPEN     : GROUP.NOK,
        SUBSTATE.NOT_OP_INITIALIZING   : GROUP.BUZY,
        SUBSTATE.NOT_OP_FAILURE        : GROUP.ERROR,
        SUBSTATE.OP_DISABLING          : GROUP.BUZY, 
        SUBSTATE.OP_CLOSING            : GROUP.BUZY, 
        SUBSTATE.OP_OPENING            : GROUP.BUZY,
        SUBSTATE.OP_FAILURE            : GROUP.ERROR,
        SUBSTATE.OP_CLOSED             : GROUP.OK, 
        SUBSTATE.OP_OPEN               : GROUP.OK,    
    })
    


class ERROR(EnumTool, int,  Enum):
    OK				      = _inc(0)
    HW_NOT_OP             = _inc()			
    INIT_FAILURE          = _inc()	
    UNEXPECTED_CLOSED     = _inc()	
    UNEXPECTED_NONE       = _inc()	
    UNEXPECTED_OPENED     = _inc()	
    FAULT_SIG             = _inc()	
    BOTH_SIG_ACTIVE       = _inc()
    TIMEOUT_ENABLE        = _inc()
    TIMEOUT_DISABLE       = _inc()
    TIMEOUT_INIT          = _inc()
    TIMEOUT_CLOSE         = _inc()
    TIMEOUT_OPEN          = _inc()
    
    SIM_NOT_INITIALISED		= 90
    SIM_NULL_POINTER		= 100	# Simulator error
    
    UNREGISTERED = -9999

# Add text definition to each constants, the definition is then accessible throught .txt attribute     
enum_txt ({
    ERROR.OK:				   'OK',
    ERROR.HW_NOT_OP:		   'ERROR: TwinCAT not in OP state or CouplerState not mapped.',
    ERROR.INIT_FAILURE:	       'ERROR: INIT command aborted due to STOP or RESET.',
    ERROR.UNEXPECTED_CLOSED:   'ERROR: Shutter unexpectedly closed.',
    ERROR.UNEXPECTED_NONE:     'ERROR: Unexpectedly no OPEN or CLOSED signal active.',
    ERROR.UNEXPECTED_OPENED:   'ERROR: Shutter unexpectedly opened.',
    ERROR.FAULT_SIG:		   'ERROR: Fault signal active.',
    ERROR.BOTH_SIG_ACTIVE:     'ERROR: Both OPEN and CLOSED signals active.',
    ERROR.TIMEOUT_ENABLE:	   'ERROR: ENABLE timed out.',
    ERROR.TIMEOUT_DISABLE:     'ERROR: DISABLE timed out.',
    ERROR.TIMEOUT_INIT:	       'ERROR: INIT timed out.',
    ERROR.TIMEOUT_CLOSE:	   'ERROR: CLOSE timed out.',
    ERROR.TIMEOUT_OPEN:		   'ERROR: OPEN timed out.',
    ERROR.SIM_NOT_INITIALISED: 'ERROR: Shutter simulator not initialised.',
    ERROR.SIM_NULL_POINTER:	   'ERROR: NULL pointer to Shutter.',
    
    ERROR.UNREGISTERED:        'ERROR: Unregistered Error'
})

class RPC_ERROR(EnumTool, int, Enum):
    OK =  0
    NOT_OP				= -1			
    NOT_NOTOP_READY		= -2			
    NOT_NOTOP_NOTREADY	= -3	
    STILL_OPENING = -4
    STILL_CLOSING = -5
    LOCAL = -6
    
    UNREGISTERED = -9999
    
enum_txt ({ # copy past on MgetRpcErrorTxt in PLC
        RPC_ERROR.OK:					 'OK',
	    RPC_ERROR.NOT_OP:				 'Cannot control shutter. Not in OP state.',
	    RPC_ERROR.NOT_NOTOP_READY:	     'Call failed. Not in NOTOP_READY.',
	    RPC_ERROR.NOT_NOTOP_NOTREADY:	 'Call failed. Not in NOTOP_NOTREADY/ERROR.',
	    RPC_ERROR.STILL_OPENING:		 'Not allowed to close the shutter while opening.',
	    RPC_ERROR.STILL_CLOSING:		 'Not allowed to open the shutter while closing.',
	    RPC_ERROR.LOCAL:				 'RPC calls not allowed in Local mode.',
        
        RPC_ERROR.UNREGISTERED:          'Unregistered RPC Error',
})





#  ____        _          __  __           _      _ 
# |  _ \  __ _| |_ __ _  |  \/  | ___   __| | ___| |
# | | | |/ _` | __/ _` | | |\/| |/ _ \ / _` |/ _ \ |
# | |_| | (_| | || (_| | | |  | | (_) | (_| |  __/ |
# |____/ \__,_|\__\__,_| |_|  |_|\___/ \__,_|\___|_|
# 


class ShutterCfgData(EltDevice.Data.CfgData):
    low_closed:     NodeVar[bool] = Field(False, description="cfg.bActiveLowClosed")
    low_fault:      NodeVar[bool] = Field(False, description="cfg.bActiveLowFault")
    low_open:       NodeVar[bool] = Field(False, description="cfg.bActiveLowOpen")
    low_switch:     NodeVar[bool] = Field(False, description="cfg.bActiveLowSwitch")
    ignore_closed:  NodeVar[bool] = Field(False, description="cfg.bIgnoreClosed")
    ignore_fault:   NodeVar[bool] = Field(False, description="cfg.bIgnoreFault")
    ignore_open:    NodeVar[bool] = Field(False, description="cfg.bIgnoreOpen")
    initial_state:  NodeVar[bool] = Field(False, description="cfg.bInitialState")
    timeout:        NodeVar[int] = Field(3000  , description="cfg.nTimeout")
    
    
class ShutterStatData(EltDevice.Data.StatData):    
    local:      NodeVar[bool] = Field(False, description="True if the device is local mode")
    error_code: NodeVar[int] = 0 

class ShutterData(EltDevice.Data):        
    StatData = ShutterStatData
    CfgData = ShutterCfgData
    
    cfg: CfgData = CfgData()
    stat: StatData = StatData() 


#  _       _             __                
# (_)_ __ | |_ ___ _ __ / _| __ _  ___ ___ 
# | | '_ \| __/ _ \ '__| |_ / _` |/ __/ _ \
# | | | | | ||  __/ |  |  _| (_| | (_|  __/
# |_|_| |_|\__\___|_|  |_|  \__,_|\___\___|

@record_class
class ShutterStatInterface(EltDevice.StatInterface):
    class Config(EltDevice.StatInterface.Config):
        type: str = 'Shutter.Stat'
    Data = ShutterStatData
    ERROR = ERROR
    SUBSTATE = SUBSTATE
    
    @NodeAlias1.prop("is_ready", "substate")
    def is_ready(self, substate):
        """ True if device is ready """
        return substate in [self.SUBSTATE.NOT_OP_READY_OPEN, self.SUBSTATE.NOT_OP_READY_CLOSED]
    
    @NodeAlias1.prop("is_not_ready", "substate")
    def is_not_ready(self, substate):
        """ True if device is not ready """
        return substate in [self.SUBSTATE.NOT_OP_NOT_READY]
    
    @NodeAlias1.prop("is_open", "substate")
    def is_open(self, substate):
        """ True if shutter is OPEN  """
        return substate in [self.SUBSTATE.OP_OPEN, self.SUBSTATE.NOT_OP_READY_OPEN]
    
    @NodeAlias1.prop("is_closed", "substate")
    def is_closed(self, substate):
        return substate in [self.SUBSTATE.OP_CLOSED, self.SUBSTATE.NOT_OP_READY_CLOSED]
        
    @NodeAlias1.prop("is_in_error", "substate")
    def is_in_error(self, substate: int) -> bool:
        """ -> True if device is in error state:  NOP_ERROR or OP_ERROR """
        return substate in [self.SUBSTATE.NOT_OP_FAILURE, self.SUBSTATE.OP_FAILURE]
            
@record_class
@buildproperty(EltNode.prop, 'parser') 
class ShutterCfgInterface(EltDevice.CfgInterface):
    class Config(EltDevice.CfgInterface.Config):
        type: str = 'Sutter.Cfg'
    
    Data = ShutterCfgData
    # we can define the type to parse value directly on the class by annotation
    # The @buildproperty takes care of it
    timeout: UInt32  

@record_class
class ShutterRpcInterface(EltDevice.RpcInterface):
    class Config(EltDevice.RpcInterface.Config):
        type: str = 'Shutter.Rpc'
    RPC_ERROR = RPC_ERROR
    

#      _            _          
#   __| | _____   _(_) ___ ___ 
#  / _` |/ _ \ \ / / |/ __/ _ \
# | (_| |  __/\ V /| | (_|  __/
#  \__,_|\___| \_/ |_|\___\___|
#
@record_class
class Shutter(EltDevice):
    SUBSTATE = SUBSTATE
    Config = ShutterConfig
    Data = ShutterData
    
    StatInterface = ShutterStatInterface
    CfgInterface = ShutterCfgInterface
    RpcInterface = ShutterRpcInterface
    
    stat = StatInterface.prop('stat')    
    cfg  = CfgInterface.prop('cfg')
    rpc  = RpcInterface.prop('rpc')
    
    def open(self) -> EltNode:
        """ open the shutter 
        
        Returns:
            is_open:  the :class:`NodeAlias` .stat.is_open to check if the shutter is open
        
        Example:
        
            ::
            
                wait( shutter.open() )
        """
        self.rpc.rpcOpen.rcall()    
        return self.stat.is_open 
        
    def close(self) -> EltNode:
        """ close the shutter 
        
        Returns:
            is_closed:  the :class:`NodeAlias` .stat.is_closed to check if the shutter is closed
        
        Example:
        
            ::
            
                wait( shutter.close() )
        """
        self.rpc.rpcClose.rcall()
        return self.stat.is_closed 
        
    def stop(self):
        """ stop any motion """
        self.rpc.rpcStop.rcall()


