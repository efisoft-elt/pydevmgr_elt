from pydevmgr_core import buildproperty, RpcError, NodeVar, record_class, kjoin
from ..base.eltdevice import EltDevice, GROUP

from ..base.tools import enum_group, enum_txt, EnumTool

from pydevmgr_ua import Int32, Int16
from ..base.eltnode import EltNode
from ..base.eltrpc import EltRpc

from ..base import io
from . import trk
from .motor import Motor
from enum import Enum


from typing import  List, Optional, Dict, Any
from pydantic import root_validator, BaseModel, validator, Field
# 
#   ____ ___  _   _ _____ ___ ____ 
#  / ___/ _ \| \ | |  ___|_ _/ ___|
# | |  | | | |  \| | |_   | | |  _ 
# | |__| |_| | |\  |  _|  | | |_| |
#  \____\___/|_| \_|_|   |___\____|
# 



class AxisConfig(BaseModel):
    """ Configuration for one Axis """
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    name : str = ""
    prefix  : str = ""
    cfgfile : str = ""
    config  : Motor.Config = None
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    class Config:                 
        validate_assignment = True 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Validator Functions
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~       
    @validator('config', always=True, pre=True)
    def load_config(cls, config, values):
        """ validate config attribute : if None load it from cfgfile attribute """
        if config is None:
            cfg_d = io.load_config(values['cfgfile'])        
            try:
                cfg = cfg_d[values['name']]
            except KeyError:
                raise ValueError(f'could no found {values["name"]} inside {values["cfgfile"]}')
            return Motor.Config.from_cfgdict(cfg)
# ####################################################################

    
class AdcCtrlConfig(EltDevice.Config.CtrlConfig):
    """ ctrl_config configuration for ADC """
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure (on Top of EltDevice CtrlConfig)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    latitude  : Optional[float] = -0.429833092 
    longitude : Optional[float] = 1.228800386
    axes : List[str] = [] # name of axes 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
class AdcConfig(EltDevice.Config):
    """ Adc configuration With axis list and ctrl_config re-defined """
    CtrlConfig = AdcCtrlConfig
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure (on Top of EltDeviceConfig)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    type: str = "Adc"
    ctrl_config : CtrlConfig = CtrlConfig() 
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Method to save back the configuration     
    def cfgdict(self):
        d = self.dict(exclude={'map','addres','axes','ctrl_config'})
        d.update(address=str(self.address), 
                 ctrl_config=self.ctrl_config.cfgdict(),                 
                 )
        return d
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Validator Functions
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @root_validator(pre=1)
    def check_axes(cls, values):
        try:
            axis_names = values['ctrl_config']['axes']
        except KeyError:
            raise ValueError('ctrl_config.axes missing')
                
        device_map = {}
        for name in axis_names:
            try:
                axis_def = values[name]
            except KeyError:
                raise ValueError(f'no axis name {name} is defined')            
            device_map[name] = AxisConfig(name=name, **axis_def).config        
        values['device_map'] = device_map
        return values       
        
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
# RPC error
RPC_ERROR = trk.RPC_ERROR

### ##############
# errors
ERROR = trk.ERROR


class AXIS(int, Enum):
    """ AXIS enumeration has defined inside the PLC """
    ALL_AXIS = 0
    AXIS1 = 1
    AXIS2 = 2

### ############# 
# Mode 
class MODE(EnumTool, int, Enum):
    """ The three ADC modes """
    ENG   = 0 
    OFF   = 1
    AUTO  = 2

enum_group({ # associate mode to group (used for graphical representation)
    MODE.ENG    : GROUP.ENG,
    MODE.OFF	: GROUP.STATIC,
    MODE.AUTO	: GROUP.TRACKING,
})



#  ____    _  _____  _      __  __           _      _ 
# |  _ \  / \|_   _|/ \    |  \/  | ___   __| | ___| |
# | | | |/ _ \ | | / _ \   | |\/| |/ _ \ / _` |/ _ \ |
# | |_| / ___ \| |/ ___ \  | |  | | (_) | (_| |  __/ |
# |____/_/   \_\_/_/   \_\ |_|  |_|\___/ \__,_|\___|_|
#


class AdcCfgData(EltDevice.Data.CfgData):
    pslope:             NodeVar[float]  =  Field(0.0023,       description="Pressure Slope [arcsec/mBar] cfg.lrPslope")
    poffset:            NodeVar[float]  =  Field(743.0,        description="Pressure Offset [mBar] cfg.lrPoffset")
    tslope:             NodeVar[float]  =  Field(-0.0061,      description="Temperature Slope [arcsec/degC] cfg.lrTslope") 
    toffset:            NodeVar[float]  =  Field(12.0,         description="Temperature Offset [degC] cfg.lrToffset")
    afactor:            NodeVar[float]  =  Field(3.32,         description= "ADC Refraction Factor [1/arcsec] cfg.lrAfactor")  
    zdlimit:            NodeVar[float]  =  Field(0.0174533,    description=" 1.0 Deg Zenith Distance Limit [rad]")
    minelev:            NodeVar[float]  =  Field(27.54,        description="Minimum elevation [rad]  cfg.lrMinElev")
    latitude:           NodeVar[float]  =  Field(-0.429833092, description="Site Latitude")
    longitude:          NodeVar[float]  =  Field(1.228800386,  description="Site Longitude")
    trk_period:         NodeVar[int]  =  0 #cfg.nMinSkipCycles
    trk_threshold:      NodeVar[float]  =  Field(1.0, description="If maximum Error is <... traking is True [UU] cfg.lrTrkThreshold")
    mot1_signoff:       NodeVar[int]    =  Field(1,   description="sign, e.g. ADC position sign for OFF  mode cfg.unitCfg[1].nSignOff")
    mot2_signoff:       NodeVar[int]    =  Field(1,   description="sign, e.g. ADC position sign for OFF  mode cfg.unitCfg[2].nSignOff")
    mot1_signauto:      NodeVar[int]    =  Field(1,   description="sign, e.g. ADC position sign for AUTO mode cfg.unitCfg[1].nSignAuto")
    mot2_signauto:      NodeVar[int]    =  Field(1,   description="sign, e.g. ADC position sign for AUTO mode cfg.unitCfg[2].nSignAuto")
    mot1_signphi:       NodeVar[int]    =  Field(1,   description="sign, e.g. ADC sign for phi (refraction) component cfg.unitCfg[1].nSignPhi")
    mot2_signphi:       NodeVar[int]    =  Field(1,   description="sign, e.g. ADC sign for phi (refraction) component cfg.unitCfg[2].nSignPhi")
    mot1_refoff:        NodeVar[float]  =  Field(0.0, decription="Reference (offset) for OFF  mode cfg.unitCfg[1].lrRefOff")
    mot2_refoff:        NodeVar[float]  =  Field(0.0, decription="Reference (offset) for OFF  mode cfg.unitCfg[2].lrRefOff")
    mot1_refauto:       NodeVar[float]  =  Field(0.0, decription="Reference (offset) for AUTO mode cfg.unitCfg[1].lrRefAuto")
    mot2_refauto:       NodeVar[float]  =  Field(0.0, decription="Reference (offset) for AUTO mode cfg.unitCfg[2].lrRefAuto")
    mot1_coffset:       NodeVar[float]  =  Field(0.0, decription="Default C offset [arcsec] cfg.unitCfg[1].lrCoffset")
    mot2_coffset:       NodeVar[float]  =  Field(0.0, decription="Default C offset [arcsec] cfg.unitCfg[2].lrCoffset")
    mot1_poffset:       NodeVar[float]  =  Field(0.0, decription="Default Position offset [deg] cfg.unitCfg[1].lrPosOffset")
    mot2_poffset:       NodeVar[float]  =  Field(0.0, decription="Default Position offset [deg] cfg.unitCfg[2].lrPosOffset")
    mot1_drotfactor:    NodeVar[float]  =  Field(0.0, decription="Derotator factor cfg.unitCfg[1].lrDrotFactor")
    mot2_drotfactor:    NodeVar[float]  =  Field(0.0, decription="Derotator factor cfg.unitCfg[2].lrDrotFactor")

class AdcStatData(trk.TrkStatData):    
    initialised:     NodeVar[bool] =   Field(False,    description=" stat.bInitialised")
    track_mode:      NodeVar[int] =    Field(0  ,      description=" stat.nMode")
    alpha:           NodeVar[float] =  Field(0.0 ,     description=" stat.apparent.alpha")
    delta:           NodeVar[float] =  Field(0.0 ,     description=" stat.apparent.delta")
    error_code:      NodeVar[int] =    Field(0  ,      description=" stat.nErrorCode")
    status:          NodeVar[int] =    Field(0  ,      description=" stat.nStatus")
    local:           NodeVar[bool] =   Field(False  ,  description=" stat.bLocal")

class AdcData(EltDevice.Data):    
    StatData = AdcStatData
    CfgData = AdcCfgData
    
    cfg: CfgData = CfgData()
    stat: StatData = StatData()
    

#  _       _             __                
# (_)_ __ | |_ ___ _ __ / _| __ _  ___ ___ 
# | | '_ \| __/ _ \ '__| |_ / _` |/ __/ _ \
# | | | | | ||  __/ |  |  _| (_| | (_|  __/
# |_|_| |_|\__\___|_|  |_|  \__,_|\___\___|

@record_class
class AdcStatInterface(trk.TrkStatInterface):
    class Config(EltDevice.StatInterface.Config):
        type: str = 'Adc.Stat'
    Data = AdcStatData
    
    ERROR = ERROR
    MODE = MODE
    SUBSTATE = SUBSTATE

# This decorator convert annotation to EltNode properties  with the right 'parser'
@record_class 
@buildproperty(EltNode.prop, 'parser') 
class AdcCfgInterface(EltDevice.CfgInterface):
    class Config(EltDevice.CfgInterface.Config):
        type: str = 'Adc.Cfg'
    Data = AdcCfgData
    # we can define the type to parse value directly on the class by annotation
    trk_period : Int32
    mot1_signoff:  Int32    
    mot2_signoff:  Int32    
    mot1_signauto: Int32    
    mot2_signauto: Int32    
    mot1_signphi:  Int32    
    mot2_signphi:  Int32    

# This decorator convert annotation to RpcInterface properties  with the right 'args_parser', tuple of arg types 
@record_class
@buildproperty(EltRpc.prop, 'args_parser') 
class AdcRpcInterface(EltDevice.RpcInterface):
    class Config(EltDevice.RpcInterface.Config):
        type: str = 'Adc.Rpc'
    
    RPC_ERROR = RPC_ERROR
    ##
    # the type of rpcMethod argument can be defined by annotation
    # All method args types must be defined in a tuple
    rpcMoveAbs :  (Int16, float, float)
    rpcMoveRel :  (Int16, float, float)
    rpcMoveAngle: (float,)
    rpcMoveVel:   (Int16, float,)
    rpcStartTrack : (float,)    
    
#      _            _          
#   __| | _____   _(_) ___ ___ 
#  / _` |/ _ \ \ / / |/ __/ _ \
# | (_| |  __/\ V /| | (_|  __/
#  \__,_|\___| \_/ |_|\___\___|
#
@record_class
class Adc(EltDevice,trk.Trk):
    """ Adc object  
    
    Args:
        key (str): device key (prefix of all nodes)
        config (optional, :class:`AdcConfig`, :class:`UaDeviceIOConfig`, dict)
            Device class:`AdcConfig` structure as returned by :func:`load_device_config` from a file 
            This can also be a dictionary which will be parsed into :class:`DeviceConfig`
            A :class:`UaDeviceIOConfig` is also accepted 
        uacom (optional, :class:`UaCom`): UaCom object setting the UA communication. If not given a new one is 
            created thanks to config.address attribute
        fits_prefix (str): prefix for fits keywords
        **kwargs :  **only used if config is a dictionary** kwargs overwrite any parameter in the config dictionary 
    """
    SUBSTATE = SUBSTATE
    MODE = MODE 
    ERROR = ERROR 
    
    AXIS = AXIS
    Config = AdcConfig
    Data = AdcData
    
    StatInterface = AdcStatInterface
    CfgInterface = AdcCfgInterface
    RpcInterface = AdcRpcInterface
    
    stat = StatInterface.prop('stat')    
    cfg  = CfgInterface.prop('cfg')
    rpc  = RpcInterface.prop('rpc')
    
    
    @property
    def motor1(self) -> Motor:
        return self.devices[self.config.ctrl_config.axes[0]]    
    
    @property
    def motor2(self) -> Motor:
        return self.devices[self.config.ctrl_config.axes[1]]
    
    @property
    def motors(self) -> list:
        return self.devices()
    
    def connect(self) -> None:
        """ Connect all opc-ua client to servers """
        super(Adc, self).connect()
        for m in self.motors:
            m.connect()
    
    def disconnect(self) -> None:
        """ Disconnect client from their servers """
        super(Adc, self).disconnect()
        for m in self.motors:
            m.disconnect()
            
    def get_configuration(self, **kwargs) -> Dict[EltNode,Any]:
        cfg_dict = {}
        for m in self.motors:
            cfg_dict.update( m.get_configuration() )
        
        config = self._config 
        
        ctrl_config = config.ctrl_config
        # just update what is in ctrl_config, except axes      
        cfg_dict.update( {self.cfg.get_node(k):v for k,v in ctrl_config.dict().items() if k not in ["axes"]} ) 
        cfg_dict.update( {self.cfg.get_node(k):v for k,v in  kwargs.items() } )
        return cfg_dict
    
    def init(self) -> EltNode:
        # fix a feature inside the FB_MA, the RPC_Init return silently zero even if the
        # device is not in the right state
        # TODO remove the patch when this is fixed from ESO side 
        if self.stat.substate.get() != self.SUBSTATE.NOTOP_NOTREADY:
            raise RpcError("Should be in NOTOP_NOTREADY state")
        self.rpc.rpcInit.rcall()
        return self.stat.is_ready
    
    def stop(self) -> None:
        """ Stop all ADC motions """
        self.rpc.rpcStop.rcall()
    
    def start_track(self, angle=0.0) -> EltNode:
        """ Start tracking (AUTO mode)
        
        Args:
            angle (float, optional): target angle default = 0.0
            
        Returns:
            is_tracking:  the :class:`NodeAlias` .stat.is_tracking to check if the device is in tracking  
        """
        self.rpc.rpcStartTrack.rcall(angle)
        return self.stat.is_tracking
        
    def move_angle(self, angle=0.0) -> EltNode:
        """ Move to angle  (OFF mode)
        
        Args:
            angle (float, optional): target angle default = 0.0 
            
        Returns:
            is_standstill:  the :class:`NodeAlias` .stat.is_standstill to check if the device is 
                            in standstill. (e.i. movement finished)
        
        Example:
        
            ::
            
                wait( adc.move_angle( 34.3 ) )
        """
        self.rpc.rpcMoveAngle.rcall(angle)
        return self.stat.is_standstill
        
    def move_abs(self, axis, pos, vel) -> EltNode:
        """ Move one or all motor to an absolute  position 
        
        Args:
            axis (int): 0 for all motors 1 for axis 1 and 2 for axis 2. See .AXIS enumerator attribute
            pos (float): target absolute position 
            vel (float): target velocity 
        
        Returns:
            is_standstill:  the :class:`NodeAlias` .stat.is_standstill to check if the device is in standstill
        
        Example:
        
            ::
            
                wait( adc.move_abs( adc.AXIS.AXIS1, 34.5, 4.0 ) )
        """
        self.rpc.rpcMoveAbs.rcall(axis, pos, vel)
        return self.stat.is_standstill
    
    def move_rel(self, axis, pos, vel) -> EltNode:
        """ Move one or all motor to an relative position 
        
        Args:
            axis (int): 0 for all motors 1 for axis 1 and 2 for axis 2
            pos (float): target relative position 
            vel (float): target velocity 
        
        Returns:
            is_standstill:  the :class:`NodeAlias` .stat.is_standstill to check if the device is in standstill
        
        Example:
        
            ::
            
                wait( adc.move_rel( adc.AXIS.AXIS1, 8.5, 4.0 ) )
        """
        self.rpc.rpcMoveRel.rcall(axis, pos, vel)
        return self.stat.is_standstill

    def move_vel(self, axis, vel) -> EltNode:
        """ Move one or all motor in velocity 
        
        Args:
            axis (int): 0 for all motors 1 for axis 1 and 2 for axis 2
            vel (float): target velocity 
        
        Return:
           None
        """
        self.rpc.rpcMoveVel.rcall(axis, vel)
        



#  ____        _          __  __           _      _ 
# |  _ \  __ _| |_ __ _  |  \/  | ___   __| | ___| |
# | | | |/ _` | __/ _` | | |\/| |/ _ \ / _` |/ _ \ |
# | |_| | (_| | || (_| | | |  | | (_) | (_| |  __/ |
# |____/ \__,_|\__\__,_| |_|  |_|\___/ \__,_|\___|_|
# 
