import yaml
from . import io
from .tools import    get_enum_txt
from .config import eltconfig

from .eltinterface import EltInterface
from .eltnode import EltNode
from .eltrpc import EltRpc
from .eltstat import StatInterface
from .eltengine import EltEngine 
from .register import register

from pydantic import BaseModel,  AnyUrl,  validator, Field, root_validator
from pydevmgr_core import (upload, NodeVar, open_device,  get_class, DeviceFactory, KINDS, BaseFactory) 
from pydevmgr_core.nodes import Local
from pydevmgr_ua import UaDevice
from typing import Optional



class CtrlConfig(BaseModel):
    # nothing by default to declare here 
    class Config: # BaseModel configuration of pydantic 
        # ignore/allow extra stuff for auto setup
        extra = 'allow'
        validate_assignment = True 
        
    def cfgdict(self):
        return self.dict()


class EltDeviceIO(BaseFactory):
    """ Factory which load a configuration file when building device 

    Args:
        type: str the type of the wanted object factory (e.g. 'Motor')
        cfgfile: configuration file path must be absolute or relative to one found in resources directory
        name (str, optional) : give the path to where the device is located in the configuration file. If 
                               not given the configuration file is considered as the root device configuration
        
    """
    type: str
    cfgfile: str
    name: Optional[str] = None
    def build(self, parent=None, name=None):
        file_path = self.cfgfile
        if self.name:
           file_path += "("+self.name+")"
        cls = get_class(KINDS.DEVICE, self.type)
        cfg = io.load_config(file_path)        
        cfg = cls.Config.parse_obj(cfg)
        for key, val in self.dict( exclude=set(["name", "cfgfile", "type"]) ).items():
            setattr(cfg, key, val)
        return cfg.build( parent, name= name or self.name)
        
class EltDeviceConfig(UaDevice.Config):
    CtrlConfig = CtrlConfig
    Interface = EltInterface.Config
    Node = EltNode.Config
    Rpc = EltRpc.Config
    Stat = StatInterface.Config # comes with some default   
    Cfg  = EltInterface.Config
    Rpcs = EltInterface.Config
    # ###############################################
    type: str = "Elt"
    # address : AnyUrl = Field( default_factory = lambda : eltconfig.default_address)
    @property
    def dev_endpoint(self): # read only property to handle ELT V4 version 
        return self.address

    fits_prefix : str            = ""    
    ignored     : bool           = False  
    ctrl_config : CtrlConfig     = CtrlConfig()
    mapfile: Optional[str] = ""
    
    identifier: str = "PLC1"
    alias: str = ""
    simulated: bool = False
    interface: str = "Softing"
    sim_endpoint: str = ""

    stat : Stat = Stat() #  a generic interface so the Base EltDevice can almost function with any interfaces
    cfg  : Cfg = Cfg() 
    Rpcs : Rpcs = Rpcs()
    
    # ###############################################
    class Config: # BaseModel configuration of pydantic 
        # ignore/allow extra stuff for auto setup
        extra = 'allow'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.mapfile:
            self.load_mapping()

    def load_mapping(self):
        if not self.mapfile:
            return 

        map_d = io.load_map(self.mapfile)
        try:
            map = map_d[self.type]
        except KeyError:
            raise ValueError("The associated map file does not contain type %r"%self.type)
        
        for k_i, d_i in map.items():
            if k_i == "rpc":
                interface = self.rpcs 
            else:
                interface = getattr(self, k_i)

            for k,s in d_i.items():
                node = getattr(interface, k)
                node.suffix = s
    
    @root_validator(pre=True)
    def _cfg_file_version_handling(cls, values):
        try:
            values['address'] = values.pop('dev_endpoint')
        except KeyError:
            pass
        return values
    


    @validator('address', pre=True)
    def _map_host(cls, url):
        """ replace the address on-the-fly if any defined in host_mapping dictionary """
        return eltconfig.host_mapping.get(url, url)
    
    @classmethod 
    def from_cfgdict(cls, config_dict):
        return cls.parse_obj(config_dict) 
    
    def cfgdict(self, exclude=set()):
        if self.version == 'pydevmgr':
            return super().cfgdict()
        
        all_exclude = {*{'version', 'address',  'device_map',  'interface_map', 'node_map', 'rpc_map','ctrl_config'}, *exclude}
        d = super().cfgdict(exclude=all_exclude)
        if 'address' not in exclude:
            d['address'] = str(self.address)
        if 'ctrl_config' not in exclude:
            d['ctrl_config'] = self.ctrl_config.cfgdict()                
        return d


def open_elt_device(cfgfile, key=None, path=0, prefix=""):
    """ open a device """
    return open_device(cfgfile, key=key, path=path, prefix=prefix) 


class RpcInterface(EltInterface):
    pass      

class CfgInterface(EltInterface):
    pass




@register
class EltDevice(UaDevice): 
    Config = EltDeviceConfig
    Engine = EltEngine 
    
    class Data(UaDevice.Data):
        Stat = StatInterface.Data
        Cfg  = CfgInterface.Data
        
        stat: Stat = Stat()
        cfg: Cfg = Cfg()
        is_ignored: NodeVar[bool] = False
     
    Node = EltNode
    Rpc = EltRpc
    Interface = EltInterface
    

    Stat = StatInterface
    Cfg  = CfgInterface
    Rpcs = RpcInterface
    
    # copy the STATE SUBSTATE here  
    STATE = Stat.STATE
    SUBSTATE = Stat.SUBSTATE
    ERROR    = Stat.ERROR
    
    @property
    def rpc(self):
        # alias for compatibility reason 
        return self.rpcs
    

    is_ignored = Local.Config(default=False)
    
    _devices = None # some device can have child devices (e.g. ADC)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_ignored.set( self.config.ignored )
        
   
    ## These RPC should be on all devices
    def init(self) -> EltNode:
        """ init the device 
        
        Raises:
            RpcError:  if OPC-UA Rpc method  returns an error code
        
        Returns: 
            is_ready:  the :class:`NodeAlias` .stat.is_ready to check if the init is finished 
        
        Example:
        
            ::
            
                wait( device.init() )
        
        """
        self.rpc.rpcInit.rcall()
        return self.stat.is_ready
        
    def reset(self) -> EltNode:
        """ reset the device 
        
        Raises:
            RpcError:  if OPC-UA Rpc method  returns an error code
        
        Returns:
           is_not_ready:  the :class:`NodeAlias` .stat.is_not_ready to check if the reset was done 
        
        ::
            
            wait( device.reset() )
        
        """
        self.rpc.rpcReset.rcall()
        return self.stat.is_not_ready

    def enable(self) -> EltNode:
        """ enable the device 
        
        Raises:
            RpcError:  if OPC-UA Rpc method  returns an error code
        
        Returns
             is_operational: the :class:`NodeAlias` .stat.is_operational to check if device was enabled 
        
        ::
            
            wait( device.enable() )
        
        """ 
        self.rpc.rpcEnable.rcall()
        return self.stat.is_operational
        
    def disable(self) -> EltNode:
        """ disable the device 
        
        Raises:
            RpcError:  if OPC-UA Rpc method  returns an error code 
             
        Returns: 
            is_not_operational:  the :class:`NodeAlias` .stat.is_not_operational to check if device was disabled 
        
        ::
            
            wait( device.disable() )
            
        """
        self.rpc.rpcDisable.rcall()
        return self.stat.is_not_operational
    
    
    def get_error_txt(self, errcode: int) -> str:
        """ Get a text description of the given error code number """
        return get_enum_txt(self.ERROR, errcode, f"Unknown Error ({errcode})")
    
    def get_rpc_error_txt(self, rpc_errcode: int) -> str:
        """ Get a text description of the given rpc error code number """
        return get_enum_txt( self.RpcInterface.RPC_ERROR, rpc_errcode, f"Unknown error ({rpc_errcode})" )
   

    def get_configuration(self, exclude_unset=True, **kwargs):
        """ return a node/value pair dictionary ready to be uploaded 
        
        The node/value dictionary represent the device configuration. 
        This is directly use by :func:`Device.configure` method. 
        
               
        Args:
            exclude_unset (optional, bool): Default is True. If True value that was left unset in 
                the config will not be included in the configuration
            \**kwargs : name/value pairs pointing to self.cfg.<name> node
                      This allow to change configuration on the fly
                      without changing the config file.             
        
        Exemples

        ::
        
            >>> upload( {**motor1.get_configuration(), **motor2.get_configuration()} ) 
        """
        # get values from the ctrl_config Config Model
        # do not include the default values, if they were unset, the PLC will use the default ones
        values = self.config.ctrl_config.dict(exclude_none=True, exclude_unset=exclude_unset)
        cfg_dict = {getattr(self.cfg,k):v for k,v in values.items()}
        cfg_dict[self.is_ignored] = self.config.ignored 
        cfg_dict.update({ getattr(self.cfg,k):v for k,v in kwargs.items()})
        return cfg_dict

    def configure(self, exclude_unset=True, **kwargs):
        """ Configure the whole device in the PLC according to what is defined in the config dictionary 
        
        Quick changes on configuration value can be done by keywords where each key must point to a 
        self.cfg.<name> node. Note that the configuration (as written in file) is always used first before being 
        overwritten by \**kwargs. In other words kwargs are not changing the default configuration in self.config.ctrl_config  
        
        Args:
            exclude_unset (optional, bool): Default is True. If True value that was left unset in 
                the config will not be included in the configuration

            \**kwargs :  name/value pairs pointing to cfg.name node
                        This allow to quickly change configuration on the fly
                        without changing the config file.
                          
        
        what it does is just:
        
        ::
        
           >>> upload( self.get_condifuration() ) 
        """
        # by default just copy the "ctrl_config" into cfg. This may not work for
        # all devices and should be customized  
        upload(self.get_configuration(exclude_unset=exclude_unset, **kwargs))
   
 
        
    
    
     
