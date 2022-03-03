from pydevmgr_core import (KINDS, NodeAlias, BaseNode, kjoin, ksplit, BaseInterface, InterfaceProperty, 
                           BaseManager, AllTrue, upload, get_device_class, open_object, get_class, record_class)

from . import io
from .eltdevice import EltDevice

from .tools import fsplit, fjoin
import logging

from collections import OrderedDict
from warnings import warn

from pydantic import BaseModel, root_validator, validator, AnyUrl
from typing import List, Type, Optional, Dict, Union, Iterable
import warnings
                        
class ManagerConfig(BaseManager.Config):
    """ Manager Configuration Model """
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    type: str = "Elt"
    server_id: str = "" # for the record
    name: str = "" # if None takes the server_id 
    
    fits_prefix: str = ""
    devices : List[str] = [] # list of device names for the record 
    cmdtout : int = 60000    # not yet used in pydevmgr 
    # ~~~~~~ Not Used by pydevmgr ~~~~~~~~~~~~~~~~~~~~~~
    req_endpoint    : str =  "zpb.rr://127.0.0.1:12082/"
    pub_endpoint    : str =  "zpb.ps://127.0.0.1:12345/"
    db_endpoint     : str =  "127.0.0.1:6379"
    db_timeout      : int =  2
    scxml           : str =  ""
    dictionaries    : List[str] =  []    
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Config of BaseModel see pydantic 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    class Config:
        extra = "ignore"
    
    @classmethod
    def from_cfgdict(cls, d):
        if d.get("version", None)=="pydevmgr":
            return cls.parse_obj(d)
        sid = d['server_id']
        ds = d[sid]
        device_map = {}
        for device in ds.get("devices", []):
            dio = d[device]
            Device = get_class( KINDS.DEVICE, dio['type'])
            device_map[device] = Device.Config.from_cfgfile(dio['cfgfile'], path=device)
        
        ds['device_map'] = device_map
        return cls.parse_obj(ds)
        
           
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Method to save back the configuration     
    def cfgdict(self):
        d = {'server_id':self.server_id, self.server_id:self.server.cfgdict()} 
        for name, ioc in self.devices.items():
            d[name] = ioc.cfgdict()
        return d

def open_elt_manager(cfgfile, key=None, path=None, prefix=""):
    """ Open a EltManager from a configuration file 

    ..note::
        
        pydevmgr is using yaml configuration file different to the ones used in ELT v3 
        However, do not wary, it will be transformed 

    Args:
        cfgfile: relative path to one of the $CFGPATH or absolute path to the yaml config file 
        key: Key of the created Manager 
        path (str, int, optional): 'a.b.c' will loock to cfg['a']['b']['c'] in the file. If int it will loock to the Nth
                                    element in the file
        prefix (str, optional): additional prefix added to the name or key

    Output:
        manager (EleManager) : elt manager handler
    """
    return EltManager.from_cfgfile(cfgfile, path=path, prefix=prefix, key=key)
    
    
class ManagerIOConfig(BaseModel):
    """ Config Model holding the I/O of a manager configuration """
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    name      : str = ""
    cfgfile   : Optional[str] = None
    config    : ManagerConfig = None # built from cfgfile if None
    extrafile : Optional[str] = None # extra is a pydevmgr thing. Used to defined guis layout for instance
    extra     : Dict = None # extracted from extrafile 
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Validator Functions
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
    @validator('config', always=True, pre=True)
    def load_config(cls, config, values):
        if config is None:
            cfgfile = values['cfgfile']
            if cfgfile:
                return ManagerConfig(name=values['name'], **io.load_config(cfgfile))
            else:
                return ManagerConfig(name=values['name'])
        return config
    
    @validator('extra', always=True, pre=True)
    def load_extra(cls, extra, values):
        if extra is None:
            extrafile = values['extrafile']
            if extrafile:
                return io.load_config(extrafile)
            else:
                cfgfile = values['cfgfile']
                if cfgfile:
                    return io.load_extra_of(cfgfile) or {}
                return {}
        return extra
    

def load_manager_config(file_name: str, extrafile: Optional[str] =None) -> ManagerIOConfig:
    """ load a manager configuration from its yml file 
    
    Args:
        file_name (str): relative path to a configuration file 
                  The path is relative to one of the directory defined in the
                  $CFGPATH environmnet variable or it can be an absolute path  
    """
    return ManagerIOConfig(cfgfile=file_name, extrafile=extrafile)



## #######################################################
#
#   Some NodeAlias for the manager 
#   These are created in the .stat UaInterface property
#

class SubstateNodeAlias(NodeAlias):
    """ Attempt to build one substate out of severals """
    SUBSTATE = EltDevice.SUBSTATE
    
    def fget(self, *substates) -> int:        
        if not substates: return self.SUBSTATE.UNKNOWN
        first = substates[0]
        if all( s==first for s in substates):
            return int(first)
        return int(self.SUBSTATE.UNKNOWN)


def get_device_state_nodes(parent):
    return sum( [[d.stat.state,d.ignored] for d in  parent.devices()], [])

##
# The stat manager for stat interface will be build of NodeAliases only 
#  
@record_class
class ManagerStatInterface(BaseInterface):
    """ Special definition of Stat Interface for a Manager """
    class Config(BaseInterface.Config):
        type: str = "UaManagerStatInterface"
        
    STATE = EltDevice.STATE
    def __init__(self, key, devices, config=None, **kwargs):
        # config is a place holder
        super().__init__(key, config=config, **kwargs)
        self._devices = devices        
        
    def devices(self) -> Iterable:
        return self._devices
    
    @classmethod
    def prop(cls, name: Optional[str] = None):
        return cls.Property(cls, cls.new, name, config=cls.Config())
        
    @classmethod
    def new(cls, parent, name, config=None):
        """ build a :class:`ManagerStatInterface` from its parent context 
        
        parent is mostlikely a :class:`UaManager`
        
        requirement for the parent is to have: 
        
        - the devices() method
        """        
        return cls(kjoin(parent.key, name), parent.devices(),config=config, **cls.new_args(parent, config))
    
    # The nodes is a function with signature func(parent) it is called by the .new class method 
    @NodeAlias.prop('state', nodes=get_device_state_nodes)
    def state(self, *states_ignore) -> int:
        """ return STATE.OP if all (not ignored) devices are in STATE.OP, STATE.NOTOP otherwhise """       
        states = [states_ignore[i] for i in range(0,len(states_ignore),2) if not states_ignore[i+1]]
                
        if all( s==self.STATE.OP for s in states ):
            return int(self.STATE.OP)
        return int(self.STATE.NOTOP)
    
    #state = DevicesState.prop('state')    
        
    @NodeAlias.prop("state_txt", ["state"])
    def state_txt(self, state: int) -> str:
        """ text representation of the state """        
        return self.STATE(state).txt
    
    @NodeAlias.prop("state_group", ["state"])
    def state_group(self, state: int) -> state:
        """ group of the state """
        return self.STATE(state).group

@record_class            
class EltManager(BaseManager):
    """ UaManager object, handling several devices 
    
    .. note::
    
        Most likely the UaManager will be initialized by :meth:`UaManager.from_config` or its alias :func:`open_elt_manager`
    
    If :meth:`UaManager.from_config` or :func:`open_elt_manager` is used all the device prefixes will be
    the key of the device manager.  
    
    Args:
        key (str): the key (prefix of all devices) of the manager
                   If None key is the 'server_id' defined inside the config dictionary
        config (dict, :class:`ManagerConfig`, :class:`ManagerIOConfig`): if dictionary it is 
        
        com_manager (:class:`UaComManager`, optional)
        
        devices (dict, optional) pairs of 
                    - name/ :class:`UaDevice` pairs 
                    - or  name/ :class:`DeviceConfig` pairs 
                    - or  name/ :class:`UaDeviceIOConfig` pairs 
                    
        extra (dict, Optional): extra configuration for GUI layout definition. a pydevmgr feature (not ESO)            
                If None can be extracted from  ``devices`` if it is a class:`ManagerIOConfig`          
    """
    
    Device = EltDevice # default device class
    Config = ManagerConfig    
    
    StatInterface = ManagerStatInterface    
    stat = StatInterface.prop('stat')
        
    def __init__(self, 
          key : Optional[str] = None, 
          config : Union[ManagerConfig,ManagerIOConfig, Dict] = None, 
          devices: Optional[Union[Dict[str, EltDevice.Config], Dict[str, EltDevice]]] = None, 
          extra : Optional[Dict] =None,
           **kwargs
        ) -> None:
        
        super().__init__(key, config=config, devices=devices, **kwargs)                
        self._extra = {} if extra is None else extra
                    
        
        
    # def __getattr__(self,attr):
    #     """ whatever is defined in __dict__ if failed try for a device name """
    #     try:
    #         return self.__dict__[attr]
    #     except KeyError:
    #         try:
    #             return self.get_device(attr)
    #         except ValueError:
    #             raise AttributeError("%r"%attr)
    
    def __dir__(self):
        lst = [d.name for d in self.devices]
        for sub in self.__class__.__mro__:
            for k in sub.__dict__:
                if not k.startswith('_'):
                    lst.append(k)
        return lst 
    
    @classmethod
    def from_cfgfile(cls, cfgfile, path="", prefix: str = '', key=None):
        return super().from_cfgfile( cfgfile, path=path, prefix=prefix, key=key)
    
    @property
    def key(self) -> str:
        return self._key
    
    # @property
    # def prefix(self):
    #     return ksplit(self._key)[0]
    
    @property
    def name(self) -> str:
        return ksplit(self._key)[1]
    
    @property
    def extra(self) -> dict:
        return self._extra
    
    def active_devices(self):
        """ return an iterator on active, aka, not-ignored devices """
        for d in self.devices:
            if not d.ignored.get():
                yield d
        
    def get_device(self, name: str) -> EltDevice:
        """ get device matching the name Raise ValueError if not found 
        Args:
           name (str): device name 
        """
        try:
            return self.devices[name]
        except KeyError:
            raise ValueError('Unknown device %r'%name)
    
    # @property
    # def devices(self) -> Iterable:
    #     """ an Iterable object of children :class:`UaDevice` like object """
    #     return DeviceIterator(self._devices)
    #     #return list(self._devices.values())

    def device_names(self) -> list:
        """ return a list of child device names """
        return self.devices.names()
    
    ## These RPC should be on all devices
    def init(self) -> NodeAlias:
        """ Init all child devices 
        
        devices with a ignored flag will be ignored 
        
        Returns:
            all_initialised: a :class:`NodeAlias` which result in True when all devices are initialised
                             can be used in the :func:`pydevmgr.wait` function 
            
        Example:
           
           ::
           
               wait( mgr.init() )
        """
        nodes = [device.init() for device in self.devices if not device.ignored.get()]
        return AllTrue('init_all_finished', nodes)
        
    def enable(self) -> NodeAlias:
        """ Enable all child devices 
        
        devices with a ignored flag will be ignored 
        
        Returns:
            all_enabled: a :class:`NodeAlias` which result in True when all devices are enabled
                             can be used in the :func:`pydevmgr.wait` function 
            
        Example:
           
           ::
           
               wait( mgr.enable() )        
        
        """
        nodes = [device.enable() for device in self.devices if not device.ignored.get()]
        return AllTrue('enable_all_finished', nodes)
        
    def disable(self) -> NodeAlias:
        """ Disable all child devices 
        
        devices with a ignored flag will be ignored 
        
        Returns:
            all_disabled: a :class:`NodeAlias` which result in True when all devices are disabled 
                             can be used in the :func:`pydevmgr.wait` function 
            
        Example:
           
           ::
           
               wait( mgr.disable_all() )   
        """
        nodes = [device.disable() for device in self.devices if not device.ignored.get()]
        return AllTrue('disable_all_finished', nodes)        

    def reset(self) -> NodeAlias:
        """ Reset all child devices 
        
        devices with a ignored flag will be ignored 
        
        Returns:
            all_reseted: a :class:`NodeAlias` which result in True when all devices are reseted
                             can be used in the :func:`pydevmgr.wait` function 
            
        Example:
           
           ::
           
               wait( mgr.reset() )   
        
        """
        nodes = [device.reset() for device in self.devices if not device.ignored.get()]
        return AllTrue('reset_all_finished', nodes)        
    
    def configure(self) -> None:
        """ Configure all devices 
        
        devices with a ignored flag will be ignored 
        """
        conf = {}
        for device in self.devices:
            if not device.ignored.get():
                conf.update( device.get_configuration() )
        upload(conf)
    
    
    def ignore_all(self):
        """ set ignored flag to True for  all devices """
        for device in self.devices:
            device.ignored.set(True)
    
    def unignore_all(self):
        """ set ignored flag to False for  all devices """
        for device in self.devices:
            device.ignored.set(False)
    
    ### deprecated 
    def connect_all(self) -> None:
        """ Deprecated use connect instead  """
        warn(DeprecationWarning("connect_all method will be removed use connect "))
        return self.connect()
    def disconnect_all(self) -> None:
        """ Deprecated use disconnect instead  """
        warn(DeprecationWarning("disconnect_all method will be removed use disconnect "))
        return self.disconnect()
    def init_all(self) -> NodeAlias:
        """ Deprecated use init instead  """
        warn(DeprecationWarning("init_all method will be removed use init "))
        return self.init()
    def enable_all(self) -> NodeAlias:
        """ Deprecated use enable instead  """
        warn(DeprecationWarning("enable_all method will be removed use enable "))
        return self.enable()
    def disable_all(self) -> NodeAlias:
        """ Deprecated use disable instead  """
        warn(DeprecationWarning("disable_all method will be removed use disable "))
        return self.disable()
    def reset_all(self) -> NodeAlias:
        """ Deprecated use reset instead  """
        warn(DeprecationWarning("reset_all method will be removed use reset "))
        return self.reset()
    def configure_all(self) -> None:
        """ Deprecated use configure instead  """
        warn(DeprecationWarning("configure_all method will be removed use configure "))
        return self.configure()    
    
   
