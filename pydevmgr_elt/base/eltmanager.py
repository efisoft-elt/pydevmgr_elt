import weakref
from pydevmgr_core import (KINDS, NodeAlias, kjoin, ksplit, BaseInterface,  
                           BaseManager, upload,   get_class,  
                           BaseDevice, NodeVar,  
                           ObjectDict, BaseFactory, 
                           create_data_class
                        )
from pydevmgr_core import BaseData, BaseNodeAlias
from pydevmgr_core.nodes import AllTrue
from pydevmgr_core.decorators import nodealias
from pydevmgr_core.io import open_manager 
from systemy import FactoryList, FactoryDict

from . import io
from .eltdevice import EltDevice, EltDeviceIO
from .eltengine import EltManagerEngine 
from .register import register 
from .tools import  get_txt, get_group
import logging

from collections import OrderedDict
from warnings import warn

from pydantic import create_model, BaseModel, root_validator, validator, AnyUrl
from typing import Any, Iterator, List, Tuple, Type, Optional, Dict, Union, Iterable
import warnings




class EltDeviceFactory(EltDeviceIO):
    cfgfile: Optional[str] = None
    def build(self, parent=None, name=None):
        if not self.cfgfile:
            Factory = get_class(KINDS.DEVICE, self.type).Config
            return Factory( **self.dict( exclude=set(["name", "cfgfile"])) ).build(parent, name) 
        else:
            return super().build(parent, name) 

class ManagerServerConfig(BaseModel):
    fits_prefix: str = ""
    devices : List[EltDeviceFactory] = [] # list of device names for the record 
    cmdtout : int = 60000    # not yet used in pydevmgr 
    # ~~~~~~ Not Used by pydevmgr ~~~~~~~~~~~~~~~~~~~~~~
    req_endpoint    : str =  "zpb.rr://127.0.0.1:12082/"
    pub_endpoint    : str =  "zpb.ps://127.0.0.1:12345/"
    db_endpoint     : str =  "127.0.0.1:6379"
    db_timeout      : int =  2
    scxml           : str =  ""
    dictionaries    : List[str] =  []    
    


class DeviceIoConfig(BaseModel):
    type: str
    cfgfile: str
    path: Optional[str] = None
    
    def load(self):
        DeviceClass = get_class(KINDS.DEVICE, self.type)
        
        cfg = io.load_config(self.cfgfile)
        if self.path is not None:
            cfg = cfg[self.path]
        return DeviceClass.Config.parse_obj(cfg)


class ManagerConfig(BaseManager.Config):
    """ Manager Configuration Model """
    Server = ManagerServerConfig
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    type: str = "Elt"
    server_id: str = "" # for the record
    name: str = "" # if None takes the server_id 
    
    server: ManagerServerConfig = ManagerServerConfig()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Config of BaseModel see pydantic 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #class Config:
    #    extra = "allow"


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # root validator 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # first load the server on the fly if server_id is defined 
    # then, at the end, load the devices
    
    @root_validator(pre=True)
    def _pre_root_validator(cls, values):
        # load the server dictionary by loadding from the server_id keyword and its attached 
        # dictionary. As it was defined in eso software <v3
        if not "server" in values and "server_id" in values:
            server_id = values["server_id"]
            values["server"] = values.pop(server_id)
        return values  
    
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
    return open_manager(cfgfile, path=path, prefix=prefix, key=key , Factory=EltManager.Config)
    # return EltManager.from_cfgfile(cfgfile, path=path, prefix=prefix, key=key)
    
    
class ManagerIOConfig(BaseModel):
    """ Config Model holding the I/O of a manager configuration """
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    name      : str = ""
    cfgfile   : Optional[str] = None
    config    : ManagerConfig = None # built from cfgfile if None
    
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


##
# The stat manager for stat interface will be build of NodeAliases only 
#  
class ManagerStatInterface(BaseInterface):
    """ Special definition of Stat Interface for a Manager """
    STATE = EltDevice.STATE
    
    class StateAlias(BaseNodeAlias):
        STATE = EltDevice.STATE

        """ Compute a State for all devices combined """
        @staticmethod
        def manager_ref():
            return None
        
        @classmethod
        def new(cls, parent, name, config=None):
            new = super().new(parent, name, config)
            new.manager_ref = parent.parent_ref
            return new

        def nodes(self):
            for device in self.manager_ref().devices:
                if not device.is_ignored.get():
                    yield device.stat.state
                    
            
        def fget(self, *states):
            if all( s==self.STATE.OP for s in states ):
                return int(self.STATE.OP)
            return int(self.STATE.NOTOP)
    state = StateAlias.Config() 

    @staticmethod
    def parent_ref():
        return None
    
    @property
    def devices(self):
        self.parent_ref().devices 
        
    @classmethod
    def new(cls, parent, name, config=None):
        new = super().new(parent, name, config)
        new.parent_ref = weakref.ref(parent)
        return new
    
    @nodealias("state")
    def state_txt(self, state: int) -> str:
        """ text representation of the state """        
        return get_txt(self.STATE(state))
    
    @nodealias("state")
    def state_group(self, state: int) -> state:
        """ group of the state """
        return get_group(self.STATE(state))
    
    @nodealias("state")
    def state_info(self, state: int) -> Tuple[int, str, str]:
        """ Return (code, text, group) state """
        return (state, 
                get_txt(self.STATE(state)), 
                get_group(self.STATE(state))
            )

   
    class Data(BaseInterface.Data):
        state: NodeVar[int] = 0 
        state_txt: NodeVar[str] = ""
        state_group: NodeVar[str] = ""

@register            
class EltManager(BaseManager):
    """ UaManager object, handling several devices 
    
    .. note::
    
        Most likely the UaManager will be initialized by :meth:`UaManager.from_cfgfile` or its alias :func:`open_elt_manager`
    
       
    Args:
        key (str, optional): the key (prefix of all devices) of the manager
                   If None key is the 'server_id' defined inside the config dictionary or a random one is generated
        config (dict, :class:`ManagerConfig`, :class:`ManagerIOConfig`):  tion for the manager        
        
        devices (dict, optional) pairs of 
                    - name/ :class:`UaDevice` pairs 
                    - or  name/ :class:`DeviceConfig` pairs 
                Used when the manager is built without configuration file

    Exemples:

    ::

        from pydevmgr_elt import EltManager, Motor, Lamp
         
        devices = dict(
            motor = Motor('motor', address="opc.tcp://localhost:4840", prefix="MAIN.Motor1" ), 
            lamp = Lamp( 'lamp', address="opc.tcp://localhost:4840", prefix="MAIN.Lamp1"  )
        )
        mgr = EltManager('mgr',  devices )

        mgr.connect()
        mgr.motor.stat.pos_actual.get()
        # etc ...
        

    Or one can subclass the EltManager to configure the device layout configuration in the class 
    
    ::
        
         from pydevmgr_elt import EltManager, Motor, Lamp,  wait 
        
         class AitBench(EltManager):
            class Config( EltManager.Config, extra="forbid" ):
                motor: Motor.Config = Motor.Config( address="opc.tcp://myplc.local:4840", prefix="MAIN.Motor1" )
                lamp: Lamp.Config = Lamp.Config( address="opc.tcp://myplc.local:4840", prefix="MAIN.Lamp1" )
                server =  EltManager.Config.Server( devices=['motor', 'lamp'] )
                
                

         mgr = AitBench('mgr')
         mgr.connect()
         wait( mgr.init() )
         # etc ... 

    Above the devices list is the list of device names used in any function of mgr (like connect, init, reset etc...).
    For compatibility with ESO config file   this `device`` parameter is inside a ``server`` structure (pydandic model). This is not
    convenient but you can do whatever you want in your Config file and add the devices property of your class.  

    ::

         from pydevmgr_elt import EltManager, Motor, Lamp, CcsSim,  wait, BaseManager
         from typing import List    
         class AitBench(EltManager):
            class Config( BaseManager.Config, extra="forbid" ):
                motor: Motor.Config = Motor.Config( address="opc.tcp://myplc.local:4840", prefix="MAIN.Motor1" )
                lamp: Lamp.Config = Lamp.Config( address="opc.tcp://myplc.local:4840", prefix="MAIN.Lamp1" )
                ccs: CcsSim.Config = CcsSim.Config(address="opc.tcp://myplc.local:4840", prefix="MAIN.ccs_sim")
                devices: List[str] = ['lamp', 'motor']
             
            @property
            def devices(self):
                return [getattr(self, name) for name in self.config.devices]

         mgr = AitBench('mgr')
         mgr.devices
    
    Note, above I have added a ccs to show that even if it is not part of the devices list (used in connect, init,
    reset, enable, disable function) the ccs is still part of the manager :

    ::
        
        mgr.ccs.set_coordinates( 044534.0, -244567.0, 2000 )
        
    """
    Device = EltDevice # default device class
    DeviceFactory = EltDeviceFactory

    Config = ManagerConfig    
    
    StatInterface = ManagerStatInterface    
    stat = StatInterface.Config()
        
    def __init__(self, 
          key : Optional[str] = None, 
          config : Union[ManagerConfig,ManagerIOConfig, Dict] = None, 
          devices: Optional[Union[Dict[str, EltDevice.Config], Dict[str, EltDevice]]] = None, 
           **kwargs
        ) -> None:
       
        super().__init__(key, config=config, **kwargs)

        self._devices_dict = ObjectDict()
        
        if devices is not None:
           self._add_devices(devices)

        else:
            self._add_devices(self.config.server.devices)
        

    def __dir__(self):
        lst = [name for name in self._devices_dict]
        for sub in self.__class__.__mro__:
            for k in sub.__dict__:
                if not k.startswith('_'):
                    lst.append(k)
        return lst 
    
    def _add_devices(self, devices):
        if isinstance( devices, (dict, FactoryDict)):
            for key, obj in devices.items():
                self._add_device( key, obj)
        else:
            for obj in devices:
                self._add_device(None, obj)
                
    def _add_device(self, key, obj):
        if isinstance( obj, BaseFactory):
            device = obj.build( self, key)
        elif isinstance( obj, BaseDevice):
            device = obj
        else:
            factory = self.DeviceFactory.parse_obj(obj)
            device = factory.build( self, key)

        # self.__dict__[device.name] = device
        self._devices_dict[device.name] = device
            
    
    
    @property
    def devices(self):
        return list( self._devices_dict.values() )
        # return [getattr(self, dn) for dn in self.config.server.devices]

    @property
    def name(self) -> str:
        return ksplit(self.key)[1]
    
    
    def __getattr__(self, attr):
        try:
            return super().__getattr__(attr)
        except AttributeError:
            try:
                return self._devices_dict[attr]
            except KeyError:
                raise AttributeError(attr)
            

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
        nodes = [device.init() for device in self.devices if not device.is_ignored.get()]
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
        nodes = [device.enable() for device in self.devices if not device.is_ignored.get()]
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
        nodes = [device.disable() for device in self.devices if not device.is_ignored.get()]
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
        nodes = [device.reset() for device in self.devices if not device.is_ignored.get()]
        return AllTrue('reset_all_finished', nodes)        
    
    def configure(self) -> None:
        """ Configure all devices 
        
        devices with a ignored flag will be ignored 
        """
        conf = {}
        for device in self.devices:
            if not device.is_ignored.get():
                conf.update( device.get_configuration() )
        upload(conf)
    
    
    def ignore_all(self):
        """ set ignored flag to True for  all devices """
        for device in self.devices:
            device.is_ignored.set(True)
    
    def unignore_all(self):
        """ set ignored flag to False for  all devices """
        for device in self.devices:
            device.is_ignored.set(False)
   

    ### deprecated 
    def create_data_class( self, children: Iterator[str],  Base = None ) -> Type[BaseData]:
        """ deprecated use :func:pydevmgr_core.create_data_class instead """
        warn(DeprecationWarning("create_data_class method is deprecated, use create_data_class function"))

        if self.key:
            class_name= "Data_Of_"+self.key
        else:
            class_name = "ManagerData"

        return create_data_class(class_name, [getattr(self,name) for name in children ], base_class = Base ) 


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
    
   
