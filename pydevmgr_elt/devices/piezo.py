from pydevmgr_core import NodeAlias, buildproperty, NodeVar, record_class
from pydevmgr_ua import Int16, Int32
from ..base.eltdevice import EltDevice, GROUP
from ..base.tools import _inc, enum_group, enum_txt, EnumTool

from pydantic import Field
from enum import Enum
#                      _              _   
#   ___ ___  _ __  ___| |_ __ _ _ __ | |_ 
#  / __/ _ \| '_ \/ __| __/ _` | '_ \| __|
# | (_| (_) | | | \__ \ || (_| | | | | |_ 
#  \___\___/|_| |_|___/\__\__,_|_| |_|\__|
# 

class PiezoConfig(EltDevice.Config):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    type: str = "Piezo"

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



#  ____        _          __  __           _      _ 
# |  _ \  __ _| |_ __ _  |  \/  | ___   __| | ___| |
# | | | |/ _` | __/ _` | | |\/| |/ _ \ / _` |/ _ \ |
# | |_| | (_| | || (_| | | |  | | (_) | (_| |  __/ |
# |____/ \__,_|\__\__,_| |_|  |_|\___/ \__,_|\___|_|
# 

class PiezoCfgData(EltDevice.Data.CfgData):
    max_on:               NodeVar[int] = Field(0 , description= "Maximum Time For Piezo to be active [s] cfg.nMaxOn")
    num_axis:             NodeVar[int] = Field(3 , description= "Number of axis default is 3 cfg.nNumAxes")
    full_range1:          NodeVar[int] = Field(2**15-1 , description= "Digital Full range for axis 1 [DN] default=2**15-1=32767 cfg.nFullRange[0].nValue")
    full_range2:          NodeVar[int] = Field(2**15-1 , description= "Digital Full range for axis 2 [DN] default=2**15-1=32767 cfg.nFullRange[1].nValue")
    full_range3:          NodeVar[int] = Field(2**15-1 , description= "Digital Full range for axis 3 [DN] default=2**15-1=32767 cfg.nFullRange[2].nValue")
    home1:                NodeVar[int] = Field(0, description=" digital number for home pos, axis 1, cfg.nHome[0].nValue")
    home2:                NodeVar[int] = Field(0, description=" digital number for home pos, axis 2, cfg.nHome[1].nValue")
    home3:                NodeVar[int] = Field(0, description=" digital number for home pos, axis 3, cfg.nHome[2].nValue")
    lower_limit1:         NodeVar[int] = Field(100, description= "digital number for  low operational limit, axis 1, cfg.nLimitLow[0].nValue")
    lower_limit2:         NodeVar[int] = Field(100, description= "digital number for  low operational limit, axis 2, cfg.nLimitLow[1].nValue")
    lower_limit3:         NodeVar[int] = Field(100, description= "digital number for  low operational limit, axis 3, cfg.nLimitLow[2].nValue")
    upper_limit1:         NodeVar[int] = Field(32500, description= "digital number for high operational limit, axis 1, cfg.nLimitHigh[0].nValue")
    upper_limit2:         NodeVar[int] = Field(32500, description= "digital number for high operational limit, axis 2, cfg.nLimitHigh[1].nValue")
    upper_limit3:         NodeVar[int] = Field(32500, description= "digital number for high operational limit, axis 3, cfg.nLimitHigh[2].nValue")
    user_to_bit_input1:   NodeVar[float] = Field(1.0 , description= "gain conversion factor from user unit to bits, axis 1, cfg.lrUser2Bit_Get[0].lrValue")
    user_to_bit_input2:   NodeVar[float] = Field(1.0 , description= "gain conversion factor from user unit to bits, axis 2, cfg.lrUser2Bit_Get[1].lrValue")
    user_to_bit_input3:   NodeVar[float] = Field(1.0 , description= "gain conversion factor from user unit to bits, axis 3, cfg.lrUser2Bit_Get[2].lrValue")
    user_offset_input1:   NodeVar[int] = Field(0 , description= "digital number offset for user to bit convertion, axis 1, cfg.nUserOffsetBit_Get[0].nValue")
    user_offset_input2:   NodeVar[int] = Field(0 , description= "digital number offset for user to bit convertion, axis 2, cfg.nUserOffsetBit_Get[1].nValue")
    user_offset_input3:   NodeVar[int] = Field(0 , description= "digital number offset for user to bit convertion, axis 3, cfg.nUserOffsetBit_Get[2].nValue")
    user_to_bit_output1:  NodeVar[float] = Field(1.0, description= "gain conversion factor from user unit to bits for feedback, axis 1, cfg.lrUser2Bit_Set[0].lrValue")
    user_to_bit_output2:  NodeVar[float] = Field(1.0, description= "gain conversion factor from user unit to bits for feedback, axis 2, cfg.lrUser2Bit_Set[1].lrValue")
    user_to_bit_output3:  NodeVar[float] = Field(1.0, description= "gain conversion factor from user unit to bits for feedback, axis 3, cfg.lrUser2Bit_Set[2].lrValue")
    user_offset_output1:  NodeVar[int] = Field(0 , description= "digital number offset for user to bit convertion for feedback, axis 1, cfg.nUserOffsetBit_Set[0].nValue")
    user_offset_output2:  NodeVar[int] = Field(0 , description= "digital number offset for user to bit convertion for feedback, axis 2, cfg.nUserOffsetBit_Set[1].nValue")
    user_offset_output3:  NodeVar[int] = Field(0 , description= "digital number offset for user to bit convertion for feedback, axis 3, cfg.nUserOffsetBit_Set[2].nValue")
    
class PiezoStatData(EltDevice.Data.StatData):    
    local:      NodeVar[bool] = Field(False, description="True if the device is local mode")
    error_code: NodeVar[int] = 0 
    actual_pos_bit1:      NodeVar[int]   =  Field(0, description="stat.nActPosBit[0].nValue")
    actual_pos_bit2:      NodeVar[int]   =  Field(0, description="stat.nActPosBit[1].nValue")
    actual_pos_bit3:      NodeVar[int]   =  Field(0, description="stat.nActPosBit[2].nValue")
    actual_pos_user1:     NodeVar[float] =  Field(0.0, description="stat.lrActPosUsr[0].lrValue")
    actual_pos_user2:     NodeVar[float] =  Field(0.0, description="stat.lrActPosUsr[1].lrValue")
    actual_pos_user3:     NodeVar[float] =  Field(0.0, description="stat.lrActPosUsr[2].lrValue")
    mon_act_pos_bit1:     NodeVar[int] =    Field(0 , description="stat.monSetPosBit_0")
    mon_act_pos_bit2:     NodeVar[int] =    Field(0 , description="stat.monSetPosBit_1")
    mon_act_pos_bit3:     NodeVar[int] =    Field(0 , description="stat.monSetPosBit_2")
    mon_act_pos_usr1:     NodeVar[int] =    Field(0 , description="stat.monActPosUsr_0")
    mon_act_pos_usr2:     NodeVar[int] =    Field(0 , description="stat.monActPosUsr_1")
    mon_act_pos_usr3:     NodeVar[int] =    Field(0 , description="stat.monActPosUsr_2")

class PiezoData(EltDevice.Data):
    StatData = PiezoStatData
    CfgData = PiezoCfgData
        
    cfg: CfgData = CfgData()
    stat: StatData = StatData() 
    



#  _       _             __                
# (_)_ __ | |_ ___ _ __ / _| __ _  ___ ___ 
# | | '_ \| __/ _ \ '__| |_ / _` |/ __/ _ \
# | | | | | ||  __/ |  |  _| (_| | (_|  __/
# |_|_| |_|\__\___|_|  |_|  \__,_|\___\___|
@record_class
class PiezoStatInterface(EltDevice.StatInterface):
    
    class Config(EltDevice.StatInterface.Config):
        type: str = 'Piezo.Stat'
    
    Data = PiezoStatData
    # keys used by default by update_to
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

@record_class    
@buildproperty(EltDevice.Node.prop, 'parser')  
class PiezoCfgInterface(EltDevice.CfgInterface):
    class Config(EltDevice.CfgInterface.Config):
        type: str = 'Piezo.Cfg'
    
    Data = PiezoCfgData
    # we can define the type to parse value directly on the class by annotation
    max_on : Int32 
    num_axis : Int16
    full_range1: Int16  
    full_range2: Int16  
    full_range3: Int16
    home1: Int16  
    home2: Int16  
    home3: Int16
    lower_limit1: Int16  
    lower_limit2: Int16  
    lower_limit3: Int16
    upper_limit1: Int16  
    upper_limit2: Int16  
    upper_limit3: Int16
    user_offset_input1: Int16  
    user_offset_input2: Int16  
    user_offset_input3: Int16
    user_offset_output1: Int16  
    user_offset_output2: Int16  
    user_offset_output3: Int16
    
@record_class
@buildproperty(EltDevice.Rpc.prop, 'args_parser')
class PiezoRpcInterface(EltDevice.RpcInterface): 
    class Config(EltDevice.RpcInterface.Config):
        type: str = 'Piezo.Rpc'
       
    RPC_ERROR = RPC_ERROR
    ##
    # the type of rpcMethod argument can be defined by annotation
    # All args types must be defined in a tuple
    
    rpcMoveBits : (Int16,)*3
    rpcMoveUser : (float,)*3




#      _            _          
#   __| | _____   _(_) ___ ___ 
#  / _` |/ _ \ \ / / |/ __/ _ \
# | (_| |  __/\ V /| | (_|  __/
#  \__,_|\___| \_/ |_|\___\___|
#
@record_class
class Piezo(EltDevice):
    Config = PiezoConfig
    SUBSTATE = SUBSTATE
    ERROR = ERROR
    
    Data = PiezoData
    
    StatInterface = PiezoStatInterface
    CfgInterface = PiezoCfgInterface
    RpcInterface = PiezoRpcInterface
    
    stat = StatInterface.prop('stat')    
    cfg  = CfgInterface.prop('cfg')
    rpc  = RpcInterface.prop('rpc')
         
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


