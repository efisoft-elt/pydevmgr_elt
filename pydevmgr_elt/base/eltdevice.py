from . import io
from .tools import map2interface_map, enum_group, enum_txt, EnumTool
from enum import Enum
from .config import eltconfig, GROUP

from .eltinterface import EltInterface
from .eltnode import EltNode
from .eltrpc import EltRpc
from .eltstat import StatInterface

from enum import Enum
from pydantic import BaseModel,  AnyUrl,  validator, Field, root_validator
from pydevmgr_core import KINDS, get_device_class, upload, NodeVar, open_device, record_class, get_class, NodeAlias, NodeAlias1, LocalNode
from pydevmgr_ua import UaDevice
from typing import Optional, Type
import logging


def convert_eso_device_config(confdic : dict) -> dict:
    """ Convert a eso config file (v2) to a pydevmgr Device Config file """
    dtype = confdic['type']
    mapfile = confdic.get('mapfile', None)
    if mapfile is None:
        pass
    else:
        map_d = io.load_map(mapfile)
        try:
            map = map_d[dtype]
        except KeyError:
            raise ValueError("The associated map file does not contain type %r"%dtype)
    interface_map =  map2interface_map(map, Node=EltNode.Config, Rpc=EltRpc.Config, Interface=EltInterface.Config)
    confdic.update(interface_map)
    return confdic               


class CtrlConfig(BaseModel):
    # nothing by default to declare here 
    class Config: # BaseModel configuration of pydantic 
        # ignore/allow extra stuff for auto setup
        extra = 'allow'
        validate_assignment = True 
        
    def cfgdict(self):
        return self.dict()
        
class EltDeviceConfig(UaDevice.Config):
    CtrlConfig = CtrlConfig
    
    type: str = "Elt"
    address     : AnyUrl         = Field( default_factory = lambda : eltconfig.default_address)    
    fits_prefix : str            = ""    
    ignored     : bool           = False  
    ctrl_config : CtrlConfig     = CtrlConfig()
    mapfile: Optional[str] = ""
    

    Stat = EltInterface.Config
    Cfg  = EltInterface.Config
    Rpcs = EltInterface.Config
    

    stat : Stat = Stat()
    cfg  : Cfg  = Cfg() 
    Rpcs : Rpcs = Rpcs()
    
    auto_build = True
    class Config: # BaseModel configuration of pydantic 
        # ignore/allow extra stuff for auto setup
        extra = 'allow'
    
    @validator('address', pre=True)
    def _map_host(cls, url):
        """ replace the address on-the-fly if any defined in host_mapping dictionary """
        return eltconfig.host_mapping.get(url, url)
    
    @classmethod 
    def from_cfgdict(cls, config_dict):
        if config_dict.get('version', None) == 'pydevmgr':
            return config_dict
        config_dict = convert_eso_device_config(config_dict) 
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
    return open_device(cfgfile, key=key, path=path, prefix=prefix) 

def load_device_config(
      file_name : str, 
      type: str = None, 
      name: str = None, 
      Config: Optional[Type[EltDeviceConfig]] = None
    ) ->  EltDeviceConfig:
    """ load a device configuration 
    
    Args:
        file_name (str): relative path to a configuration file 
                  The path is relative to one of the directory defined in the
                  $CFGPATH environment variable
        type (str, optional): Type of the device, if not given look into the loaded file
        name (str, None): The device name in the config file. 
                        If None the first device in the loaded configuration file is taken 
    """
    
    allconfig = io.load_config(file_name)
    
    if name is None:
        # get the first key 
        name = next(iter(allconfig))
        config = allconfig[name]
    else:
        try:
            config = allconfig[name]
        except KeyError:
            raise ValueError(f"Device {name!r} does not exists on device definition file {file_name!r}")    
    
    config = convert_eso_device_config(config)
            
    if Config is None:    
        if type is None:
            try:
                type = config['type']
            except KeyError:
                raise ValueError('type is missing')
        try:
            Dev = get_device_class(type)            
        except (KeyError, ValueError):
            logging.warning(f'type {type!r} is unknown landing to a standard, empty device')                
            Dev = EltDevice
        Config = Dev.Config
    
    return Config(**config)    





    
    
class RpcInterface(EltInterface):
    pass      

class CfgInterface(EltInterface):
    pass




@record_class
class EltDevice(UaDevice):
    Config = EltDeviceConfig
    class Data(UaDevice.Data):
        StatData = StatInterface.Data
        CfgData = CfgInterface.Data
        
        stat: StatData = StatData()
        cfg: CfgData = CfgData()
        ignored: NodeVar[bool] = False
     
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
  
    # stat = StatInterface.prop('stat')    
    # cfg  = CfgInterface.prop('cfg')
    # rpcs  = Rpcs.prop('rpcs')
    
    @property
    def rpc(self):
        # alias for compatibility reason 
        return self.rpcs
    

    is_ignored = LocalNode.prop(default=False)
    
    _devices = None # some device can have child devices (e.g. ADC)
    
    def __init__(self, *args, fits_key: str = "", **kwargs):
        super().__init__(*args, **kwargs)
        self.fits_key = fits_key or self._config.fits_prefix 
        self.is_ignored.set( self.config.ignored )
        
    @classmethod
    def parse_config(cls, config, **kwargs):
        if config is None:
            # a little patch to open te device with a default mapping if config is None 
            map_d = io.load_default_map(kwargs.get('type',cls.Config.__fields__['type'].default))            
            map = next(iter(map_d.values())) 
            interface_map =  map2interface_map(map)
            kwargs.setdefault('interface_map', {}).update(interface_map)    
        return super().parse_config(config, **kwargs)
    
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
        return self.ERROR(errcode).txt
    
    def get_rpc_error_txt(self, rpc_errcode: int) -> str:
        """ Get a text description of the given rpc error code number """
        return self.RpcInterface.RPC_ERROR(rpc_errcode).txt
   

    def get_configuration(self, exclude_unset=True, **kwargs):
        """ return a node/value pair dictionary ready to be uploaded 
        
        The node/value dictionary represent the device configuration. 
        This is directly use by :func:`Device.configure` method. 
        
        This is a generic configuration dictionary and may not work on all devices. 
        This method need to be updated for special devices for instance.   
        
        Args:
            exclude_unset (optional, bool): Default is True. If True value that was left unset in 
                the config will not be included in the configuration
            \**kwargs : name/value pairs pointing to cfg.name node
                      This allow to change configuration on the fly
                      without changing the config file.             
        
        ::
        
            >>> upload( {**motor1.get_configuration(), **motor2.get_configuration()} ) 
        """
        # get values from the ctrl_config Config Model
        # do not include the default values, if they were unset, the PLC will use the default ones
        values = self.config.ctrl_config.dict(exclude_none=True, exclude_unset=exclude_unset)
        cfg_dict = {self.cfg.get_node(k):v for k,v in values.items()}
        cfg_dict[self.ignored] = self.config.ignored 
        cfg_dict.update({self.cfg.get_node(k):v for k,v in kwargs.items()})
        return cfg_dict

    def configure(self, exclude_unset=True, **kwargs):
        """ Configure the whole device in the PLC according to what is defined in the config dictionary 
        
        Quick changes on configuration value can be done by keywords where each key must point to a 
        .cfg.name node. Note that the configuration (as written in file) is always used first before being 
        overwritten by \**kwargs. In other word kwargs are not changing the default configuration  
        
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
   
 
        
    
    
     
