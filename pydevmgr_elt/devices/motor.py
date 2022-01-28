from pydevmgr_core import NodeAlias, NodeAlias1, buildproperty, NodeVar, record_class, BaseParser
from ..base.eltdevice import (EltDevice, GROUP)
from ..base.tools import _inc, enum_group, enum_txt, EnumTool
from pydevmgr_ua import Int32
from ..base.eltnode import EltNode
from ..base.eltrpc import EltRpc

from enum import Enum
from collections import OrderedDict 
from pydantic import BaseModel, validator, root_validator
from typing import List, Dict, Union, Optional, Any



class AXIS_TYPE(int, Enum):
    LINEAR = 1
    CIRCULAR =2
    CIRCULAR_OPTIMISED = 3

#   ____ ___  _   _ _____ ___ ____ 
#  / ___/ _ \| \ | |  ___|_ _/ ___|
# | |  | | | |  \| | |_   | | |  _ 
# | |__| |_| | |\  |  _|  | | |_| |
#  \____\___/|_| \_|_|   |___\____|
# 

class PositionsConfig(BaseModel):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    posnames : List = []
    tolerance: float = 1.0
    positions: Dict = OrderedDict()  # adding a dictionary for positions. Presfered than leaving it as extra 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Validator Functions
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    class Config:        
        extra = 'allow' # needed for the poses 
        validate_assignment = True
    @root_validator()
    def collect_positions(cls, values):     
        """ collectect the positions from the extras """ 
        positions = values['positions']
        for name in values['posnames']:
            if name not in positions:
                try:
                    positions[name] = float( values[name] ) 
                except (KeyError, TypeError):
                    raise ValueError(f'posname {name!r} is not defined or not a float')   
        return values 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Method to save back the configuration     
    def cfgdict(self):
        d = {'posnames': self.posnames, 'tolerance':self.tolerance}
        for p in self.posnames:
            d[p] = self.positions[p]
        return d
# ################################        
    
class SeqStepConfig(BaseModel):
    """ Data  Model for step configuration """
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    index: int =  0    
    value1: float = 0.0
    value2: float = 0.0
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~
    class Config:                
        validate_assignment = True
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Method to save back the configuration     
    def cfgdict(self):
        return self.dict(exclude={"index"})
# ################################


class InitialisationConfig(BaseModel):
    """ Config Model for the initialisation sequence """
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    sequence : List[str] = []
    END          : SeqStepConfig = SeqStepConfig(index=0) 
    FIND_INDEX   : SeqStepConfig = SeqStepConfig(index=1)
    FIND_REF_LE  : SeqStepConfig = SeqStepConfig(index=2)
    FIND_REF_UE  : SeqStepConfig = SeqStepConfig(index=3)
    FIND_LHW     : SeqStepConfig = SeqStepConfig(index=4)
    FIND_UHW     : SeqStepConfig = SeqStepConfig(index=5)  
    DELAY        : SeqStepConfig = SeqStepConfig(index=6)
    MOVE_ABS     : SeqStepConfig = SeqStepConfig(index=7)
    MOVE_REL     : SeqStepConfig = SeqStepConfig(index=8)
    CALIB_ABS    : SeqStepConfig = SeqStepConfig(index=9)
    CALIB_REL    : SeqStepConfig = SeqStepConfig(index=10)
    CALIB_SWITCH : SeqStepConfig = SeqStepConfig(index=11)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~
    class Config:                
        validate_assignment = True        
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Validator Functions
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @validator('END', 'FIND_INDEX', 'FIND_REF_LE', 'FIND_REF_UE', 'FIND_LHW', 'FIND_UHW', 
               'DELAY', 'MOVE_ABS', 'MOVE_REL', 'CALIB_ABS', 'CALIB_REL' , 'CALIB_SWITCH')
    def force_index(cls, v, field):
        """ need to write the index """        
        v.index = getattr(INITSEQ, field.name)
        return v

    @validator('sequence')
    def validate_initialisation(cls,sequence):   
        """ Validate the list of sequence """ 
        for s in sequence:
            try:
                cls.__fields__[s]
            except KeyError:
                raise ValueError(f'unknown sequence step named {s!r}')
        return sequence
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Method to save back the configuration     
    def cfgdict(self):
        d = {'sequence':self.sequence}
        for seq in self.sequence:
            d[seq] = getattr(self, seq).cfgdict()            
        return d
# ################################



class MotorCtrlConfig(EltDevice.Config.CtrlConfig):
    """ Config Model for the Motor Ctrl Configuration"""
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    velocity : float = 0.1 # mendatory because used as default for movement
    min_pos :           Optional[float] = 0.0
    max_pos :           Optional[float] = 0.0 
    axis_type :         Union[None,int,str] = "LINEAR" # LINEAR , CIRCULAR, CIRCULAR_OPTIMISED
    active_low_lstop :  Optional[bool] = False
    active_low_lhw :    Optional[bool] = False
    active_low_ref :    Optional[bool] = True
    active_low_index :  Optional[bool] = False
    active_low_uhw :    Optional[bool] = True
    active_low_ustop :  Optional[bool] = False
    brake :             Optional[bool] = False
    low_brake :         Optional[bool] = False
    low_inpos :         Optional[bool] = False
    backlash :          Optional[float] = 0.0
    tout_init :         Optional[int] = 30000
    tout_move :         Optional[int] = 12000
    tout_switch :       Optional[int] = 10000
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Validator Functions
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
    @validator('axis_type')
    def validate_axis_type(cls, ax):
        if isinstance(ax, str):
            try:
                getattr(AXIS_TYPE, ax)
            except AttributeError:
                raise ValueError(f"Unknown axis_type {ax!r}")
        if isinstance(ax, int):            
            # always return a string??
            ax = AXIS_TYPE(ax).name        
        return ax
# ################################
         
        
class MotorConfig(EltDevice.Config):
    CtrlConfig = MotorCtrlConfig
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    type: str = "Motor"
    initialisation : InitialisationConfig = InitialisationConfig()
    positions      : PositionsConfig = PositionsConfig()
    ctrl_config    : MotorCtrlConfig = MotorCtrlConfig()
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Method to save back the configuration     
    def cfgdict(self, exclude=set()):
        
        d = super().cfgdict(exclude=exclude)
        for a in ('initialisation', 'positions'):
            if a not in exclude:
                d[a] = getattr(self, a).cfgdict()   
        return d

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
    NOTOP_CLEARING_NOVRAM = 108

    NOTOP_ERROR =  199

    OP_STANDSTILL =216
    OP_MOVING = 217
    OP_SETTING_POS = 218
    OP_STOPPING = 219

    OP_ERROR =299
    
    UNREGISTERED = -9999
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


### ############
# Motor ERROR

class ERROR(EnumTool, int, Enum):
    OK	                   = _inc(0)
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
enum_txt ( {
    ERROR.OK:					 'OK',
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
    
    ERROR.UNREGISTERED:             'ERROR: Unregistered Error'
})


### ##############
# RPC error
class RPC_ERROR(EnumTool, int, Enum):
    OK =  0
    NOT_OP =  -1
    NOT_NOTOP_READY =  -2
    NOT_NOTOP_NOTREADY = -3
    LOCAL =  -4
    SW_LIMIT_LOWER = -5
    SW_LIMIT_UPPER = -6
    INIT_WHILE_MOVING = -7
    
    UNREGISTERED = -9999
    
enum_txt ( {
    RPC_ERROR.OK:					 'OK',
    RPC_ERROR.NOT_OP:				 'Cannot control motor. Not in OP state.',
    RPC_ERROR.NOT_NOTOP_READY:	     'Call failed. Not in NOTOP_READY.',
    RPC_ERROR.NOT_NOTOP_NOTREADY:	 'Call failed. Not in NOTOP_NOTREADY/ERROR.',
    RPC_ERROR.LOCAL:				 'RPC calls not allowed in Local mode.',
    RPC_ERROR.SW_LIMIT_LOWER:		 'Move rejected. Target Pos < Lower SW Limit',
    RPC_ERROR.SW_LIMIT_UPPER:		 'Move rejected. Target Pos > Upper SW Limit',
    RPC_ERROR.INIT_WHILE_MOVING:	 'Cannot INIT moving motor. Motor stopped. Retry.',
    
    RPC_ERROR.UNREGISTERED:          'Unregistered RPC Error',
})

##### ############
# Sequence
class INITSEQ(int, Enum):
    END = 0
    FIND_INDEX = 1
    FIND_REF_LE = 2
    FIND_REF_UE = 3
    FIND_LHW = 4
    FIND_UHW = 5

    DELAY = 6
    MOVE_ABS = 7
    MOVE_REL = 8
    CALIB_ABS = 9
    CALIB_REL = 10
    CALIB_SWITCH = 11

for E,v1,v2 in [
    ( INITSEQ.END,  "", "" ),
    ( INITSEQ.FIND_INDEX, "Fast Vel", "Slow Vel" ),
    ( INITSEQ.FIND_REF_LE, "Fast Vel", "Slow Vel" ),
    ( INITSEQ.FIND_REF_UE, "Fast Vel", "Slow Vel" ),
    ( INITSEQ.FIND_LHW, "Fast Vel", "Slow Vel" ),
    ( INITSEQ.FIND_UHW, "Fast Vel", "Slow Vel" ),
    ( INITSEQ.DELAY, "Delay [ms]", "" ),
    ( INITSEQ.MOVE_ABS, "Vel", "Pos" ),
    ( INITSEQ.MOVE_REL, "Vel", "Pos" ),
    ( INITSEQ.CALIB_ABS, "Pos", "" ),
    ( INITSEQ.CALIB_REL, "Pos", "" ),
    ( INITSEQ.CALIB_SWITCH, "Pos", "" ),
]:
    setattr(E, "var1", v1)
    setattr(E, "var2", v2)
del E,v1,v2





def axis_type(axis_type):
    """ return always a axis_type int number from a number or a string
    
    Raise a ValueError if the input string does not match axis type
    Example:
        axis_type('LINEAR') == 1
        axis_type(1) == 1
    """
    if isinstance(axis_type, str):
        try:
            axis_type = getattr(AXIS_TYPE, axis_type) 
        except AttributeError:
            raise ValueError(f'Unknown AXIS type {axis_type!r}')
    return Int32(axis_type)

# a parser class for axis type
@record_class
class AxisType(BaseParser):
    class Config(BaseParser.Config):
        type: str = "AxisType"
    @staticmethod
    def parse(value, config):
        return axis_type(value)   

# 
#   __                  _   _                 
#  / _|_   _ _ __   ___| |_(_) ___  _ __  ___ 
# | |_| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
# |  _| |_| | | | | (__| |_| | (_) | | | \__ \
# |_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
# 

def init_sequence_to_cfg(initialisation, INITSEQ=INITSEQ):
    """ from a config initialisation dict return a dictionary of key/value for .cfg interface """            
    
    
    # set the init sequence    
    cfg_dict = {} 
    
    init_dict = initialisation.dict(exclude_none=True, exclude_unset=True)
    if not "sequence" in init_dict:        
        return cfg_dict
    
    # reset all sequence variable
    for i in range(1,11):
        cfg_dict["init_seq{}_action".format(i)] = INITSEQ.END.value
        cfg_dict["init_seq{}_value1".format(i)] = 0.0
        cfg_dict["init_seq{}_value2".format(i)] = 0.0
        
    for stepnum, step_name in enumerate(initialisation.sequence, start=1):
        step = getattr(initialisation, step_name)
        cfg_dict["init_seq%d_action"%stepnum] = step.index
        cfg_dict["init_seq%d_value1"%stepnum] = step.value1
        cfg_dict["init_seq%d_value2"%stepnum] = step.value2    
    return cfg_dict





#  ____    _  _____  _      __  __           _      _ 
# |  _ \  / \|_   _|/ \    |  \/  | ___   __| | ___| |
# | | | |/ _ \ | | / _ \   | |\/| |/ _ \ / _` |/ _ \ |
# | |_| / ___ \| |/ ___ \  | |  | | (_) | (_| |  __/ |
# |____/_/   \_\_/_/   \_\ |_|  |_|\___/ \__,_|\___|_|
#

# This is kind of optional but gives all available data inside a structure 
# This structure can be linked to an instance of the device with pydevmgr.DataLink 
# Data Subclasses are also included inside the Data Model so everything is auto-consistant  

class MotorStatData(EltDevice.StatInterface.Data):
    """ class holding all stat data for a motor """
    
    pos_target:        NodeVar[float] = 0.0
    pos_actual:        NodeVar[float] = 0.0
    pos_error:         NodeVar[float] = 0.0
    vel_actual:        NodeVar[float] = 0.0
    scale_factor:      NodeVar[float] = 0.0
    local:             NodeVar[bool] = False
    backlash_step:     NodeVar[int] = 0
    mode:              NodeVar[int] = 0
    initialised:       NodeVar[bool] = False
    init_step:         NodeVar[int] = 0
    init_action:       NodeVar[int] = 0
    axis_ready:        NodeVar[bool] = False
    axis_enable:       NodeVar[bool] = False
    axis_inposition:   NodeVar[bool] = False
    axis_lock:         NodeVar[bool] = False
    axis_brake:        NodeVar[bool] = False
    axis_info_data1:   NodeVar[int] = 0
    axis_info_data2:   NodeVar[int] = 0
    error_code:        NodeVar[int] = 0
     
    signal_lstop:   NodeVar[bool] = False   
    signal_lhw:     NodeVar[bool] = False   
    signal_ref:     NodeVar[bool] = False   
    signal_index:   NodeVar[bool] = False   
    signal_uhw:     NodeVar[bool] = False   
    signal_ustop:   NodeVar[bool] = False 
    
    # Aliases 
    is_moving: NodeVar[bool] = False
    is_standstill: NodeVar[bool] = False
    pos_name: NodeVar[str] = ""

class MotorCfgData(EltDevice.CfgInterface.Data):
    brake:            NodeVar[bool] = False    
    backlash:         NodeVar[float] = 0.0
    axis_type:        NodeVar[int] = 0 
    
    velocity:         NodeVar[float] = 0.0
    max_pos:          NodeVar[float] = 0.0      
    min_pos:          NodeVar[float] = 0.0      
    check_inpos:      NodeVar[bool] = False
    lock:             NodeVar[bool] = False  
    lock_pos:         NodeVar[float] = 0.0      
    lock_tolerance:   NodeVar[float] = 0.0 
    disable:          NodeVar[bool] = False
    
    tout_init:          NodeVar[int] = 0 
    tout_move:          NodeVar[int] = 0 
    tout_switch:        NodeVar[int] = 0 


    low_brake:          NodeVar[bool] = False 
    low_inpos:          NodeVar[bool] = False 
    active_low_lstop:   NodeVar[bool] = False 
    active_low_lhw:     NodeVar[bool] = False 
    active_low_ref:     NodeVar[bool] = False 
    active_low_index:   NodeVar[bool] = False 
    active_low_uhw:     NodeVar[bool] = False 
    active_low_ustop:   NodeVar[bool] = False 

    exec_pre_init:      NodeVar[bool] = False 
    exec_post_init:     NodeVar[bool] = False 
    exec_pre_move:      NodeVar[bool] = False 
    exec_post_move:     NodeVar[bool] = False 

    init_seq1_action:  NodeVar[int] = 0
    init_seq1_value1:  NodeVar[float] = 0.0
    init_seq1_value2:  NodeVar[float] = 0.0
    
    init_seq2_action:  NodeVar[int] = 0
    init_seq2_value1:  NodeVar[float] = 0.0
    init_seq2_value2:  NodeVar[float] = 0.0
    
    init_seq3_action:  NodeVar[int] = 0
    init_seq3_value1:  NodeVar[float] = 0.0
    init_seq3_value2:  NodeVar[float] = 0.0
    
    init_seq4_action:  NodeVar[int] = 0
    init_seq4_value1:  NodeVar[float] = 0.0
    init_seq4_value2:  NodeVar[float] = 0.0
    
    init_seq5_action:  NodeVar[int] = 0
    init_seq5_value1:  NodeVar[float] = 0.0
    init_seq5_value2:  NodeVar[float] = 0.0

    init_seq6_action:  NodeVar[int] = 0
    init_seq6_value1:  NodeVar[float] = 0.0
    init_seq6_value2:  NodeVar[float] = 0.0

    init_seq7_action:  NodeVar[int] = 0
    init_seq7_value1:  NodeVar[float] = 0.0
    init_seq7_value2:  NodeVar[float] = 0.0

    init_seq8_action:  NodeVar[int] = 0
    init_seq8_value1:  NodeVar[float] = 0.0
    init_seq8_value2:  NodeVar[float] = 0.0

    init_seq9_action:  NodeVar[int] = 0
    init_seq9_value1:  NodeVar[float] = 0.0
    init_seq9_value2:  NodeVar[float] = 0.0

    init_seq10_action:  NodeVar[int] = 0
    init_seq10_value1:  NodeVar[float] = 0.0
    init_seq10_value2:  NodeVar[float] = 0.0    
    

class MotorData(EltDevice.Data):
    StatData = MotorStatData
    CfgData  = MotorCfgData
            
    stat: StatData = StatData()
    cfg:  CfgData  = CfgData()    
    


#  _       _             __                
# (_)_ __ | |_ ___ _ __ / _| __ _  ___ ___ 
# | | '_ \| __/ _ \ '__| |_ / _` |/ __/ _ \
# | | | | | ||  __/ |  |  _| (_| | (_|  __/
# |_|_| |_|\__\___|_|  |_|  \__,_|\___\___|
@record_class
class MotorStatInterface(EltDevice.StatInterface): 
    
    class Config(EltDevice.StatInterface.Config):
        type: str = 'Motor.Stat' # this is needed only for loading default map 
    
    ERROR = ERROR
    SUBSTATE = SUBSTATE
    Data = MotorStatData
    
    @NodeAlias1.prop("is_moving", "substate")
    def is_moving(self, substate):
        """ -> True is axis is moving """
        return substate == self.SUBSTATE.OP_MOVING

    @NodeAlias1.prop("is_standstill", "substate")
    def is_standstill(self,  substate):
        """ -> True is axis is standstill """
        return substate == self.SUBSTATE.OP_STANDSTILL
    
    _mot_positions = None# will be overwriten by Motor 
    @NodeAlias1.prop("pos_name", "pos_actual")
    def pos_name(self, pos_actual):
        if not self._mot_positions: return ''
        positions = self._mot_positions
        tol = positions.tolerance
        for pname, pos in positions.positions.items():
            if abs( pos-pos_actual)<tol:
                return pname
        return ''

# the decorator is converting annotations to UaNode.property, only parser is defined in annotation
@record_class
@buildproperty(EltNode.prop, 'parser')    
class MotorCfgInterface(EltDevice.CfgInterface):
    class Config(EltDevice.CfgInterface.Config):
        type: str = 'Motor.Cfg'
    
    Data = MotorCfgData
    # we can define the type to parse value directly on the class by annotation
    axis_type : axis_type
    #axis_type : "AxisType" # this should also work 
            
    tout_init: Int32 
    tout_move: Int32        
    tout_switch: Int32
    init_seq1_action: Int32
    init_seq2_action: Int32
    init_seq3_action: Int32
    init_seq4_action: Int32
    init_seq5_action: Int32
    init_seq6_action: Int32
    init_seq7_action: Int32
    init_seq8_action: Int32
    init_seq9_action: Int32
    init_seq10_action: Int32

# the decorator is converting annotations to UaRpc property, only args_parser are defined 
@record_class
@buildproperty(EltRpc.prop, 'args_parser')   
class MotorRpcInterface(EltDevice.RpcInterface):
    class Config(EltDevice.RpcInterface.Config):
        type: str = 'Motor.Rpc'
    
    RPC_ERROR = RPC_ERROR
    ##
    # the type of rpcMethod argument can be defined by annotation
    # All args types must be defined in a tuple
    rpcMoveAbs : (float, float)
    rpcMoveRel : (float, float)
    rpcMoveVel : (float,)

#      _            _          
#   __| | _____   _(_) ___ ___ 
#  / _` |/ _ \ \ / / |/ __/ _ \
# | (_| |  __/\ V /| | (_|  __/
#  \__,_|\___| \_/ |_|\___\___|
#

@record_class
class Motor(EltDevice):
    SUBSTATE = SUBSTATE
    ERROR = ERROR
    
    INITSEQ = INITSEQ
    AXIS_TYPE = AXIS_TYPE
    
    Data = MotorData
    Config = MotorConfig
    
    StatInterface = MotorStatInterface
    CfgInterface = MotorCfgInterface
    RpcInterface = MotorRpcInterface
        
    
    cfg  = CfgInterface.prop('cfg')
    rpc  = RpcInterface.prop('rpc')
    ##
    # bellow the stat function is decorated by the .prop
    # It finalise the construction of the interface by adding 
    # the _mot_position   
    @StatInterface.prop('stat')    
    def stat(self, interface):
        interface._mot_positions = self.config.positions
        
    
    def get_configuration(self, **kwargs) -> Dict[EltNode,Any]:
        """  return a node/value pair dictionary ready to be uploaded 
        
        The node/value dictionary represent the device configuration. 
        
        Args:
            **kwargs : name/value pairs pointing to cfg.name node
                      This allow to change configuration on the fly
                      without changing the config file. 
        """
        
        config = self._config 
        
        ctrl_config = config.ctrl_config
        # just update what is in ctrl_config, this should work for motor 
        # one may need to check parse some variable more carefully       
        values = ctrl_config.dict(exclude_none=True, exclude_unset=True)
        cfg_dict = {self.cfg.get_node(k):v for k,v in  values.items() }
        cfg_dict[self.ignored] = self.config.ignored 
        cfg_dict.update({self.cfg.get_node(k):v for k,v in  kwargs.items() })
        
        init_cfg = init_sequence_to_cfg(config.initialisation, self.INITSEQ)
        cfg_dict.update({self.cfg.get_node(k):v for k,v in init_cfg.items()})
        
        # transform axis type to number 
        if self.cfg.axis_type in cfg_dict:
            axis_type = cfg_dict[self.cfg.axis_type] 
            cfg_dict[self.cfg.axis_type] =  getattr(AXIS_TYPE, axis_type) if isinstance(axis_type, str) else axis_type
        ###
        # Set the new config value to the device 
        return cfg_dict
          
    @property
    def posnames(self) -> str:
        """ configured position names in a name:(pos, tol) dictionary """
        return self.config.positions.posnames      
            
    @property
    def velocity(self) -> float:
        return self.config.ctrl_config.velocity
    
    def clear(self) -> None:
        """ Clear cashed values """
        super(Motor, self).clear()
        self.__dict__.pop('posnames', None)
    
    def move_abs(self, absPos, vel=None) -> EltNode:
        """ move motor to an absolute position 
        
        self.move_abs(pos, vel) <-> self.rpc.rpcMoveAbs(pos, vel)
        
        Args:
            absPos (float): absolute position
            vel (float):   target velocity for the movement
            
        """
        vel = self.velocity if vel is None else vel
        self.rpc.rpcMoveAbs.rcall(absPos, vel)
        return self.stat.is_standstill
        
    def move_name(self, name, vel=None) -> EltNode:
        """ move motor to a named position 
        
        Args:
           name (str): named position
           vel (float):   target velocity for the movement
        """
        absPos = self.get_pos_target_of_name(name)
        return self.move_abs(absPos, vel)
        
    def move_rel(self, relPos, vel=None) -> EltNode:
        """ Move motor relative position
        
        Args:
           relPos (float): relative position
           vel (float):   target velocity for the movement
        """
        vel = self.velocity if vel is None else vel
        self.rpc.rpcMoveRel.rcall(relPos, vel)
        return self.stat.is_standstill
        
    def move_vel(self, vel) -> None:
        """ Move motor in velocity mode 
        
        Args:
           vel (float): target velocity
        """
        self.rpc.rpcMoveVel.rcall(vel)

    def stop(self) -> None:
        """ Stop the motor """
        self.rpc.rpcStop.rcall()
    
    def get_pos_target_of_name(self, name: str) -> float:
        """return the configured target position of a given pos name or raise error"""
        try:
            position = getattr(self.config.positions, name)
        except AttributeError:
            raise ValueError('unknown posname %r'%name)
        return position

    def get_name_of_pos(self, pos_actual: float) -> str:
        """ Retrun the name of a position from a position as input or ''
        
        Example:
            m.get_name_of( m.stat.pos_actual.get() )
        """
        positions = self.config.positions    
        tol = positions.tolerance
        
        for pname, pos in positions.positions.items():
            if abs( pos-pos_actual)<tol:
                return pname
        return ''
        
    def is_near(self, pos: float, tol: float, data: Optional[Dict[str,Any]] =None) -> bool:
        """ -> True when abs(pos_actual-pos)<tol """
        apos = self.stat.pos_actual.get(data) 
        return abs(apos-pos)<tol


