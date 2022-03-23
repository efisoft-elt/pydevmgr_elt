from pydevmgr_elt.devices.adc.stat import AdcStat as Stat
from pydevmgr_elt.devices.adc.cfg  import AdcCfg as Cfg
from pydevmgr_elt.devices.adc.rpcs import AdcRpcs as Rpcs

from pydevmgr_elt.base import EltDevice
from pydevmgr_core import record_class, Defaults, RpcError, kjoin, BaseDevice
from typing import Optional, Any, Dict, List
from pydevmgr_elt.devices.motor import Motor
from pydevmgr_elt import io
from pydevmgr_core import path_walk_item , NegNode
from pydantic import BaseModel 

Base = EltDevice


class AxisIoConfig(BaseModel):
    """ Configuration for one Axis """
    Motor = Motor.Config
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    prefix  : str = ""
    cfgfile : str = ""
    path: Optional[str] = None
    def load(self):
        cfg = io.load_config(self.cfgfile)
        if self.path is not None:
            cfg = path_walk_item(cfg, self.path)
            
        return Motor.Config.parse_obj(cfg)

class AdcCtrlConfig(Base.Config.CtrlConfig):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure (on top of CtrlConfig)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    latitude  : Optional[float] = -0.429833092 
    longitude : Optional[float] = 1.228800386
    axes : List[str] = [] # name of axes 

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
class AdcConfig(Base.Config):
    CtrlConfig = AdcCtrlConfig
    
    Cfg = Cfg.Config
    Stat = Stat.Config
    Rpcs = Rpcs.Config
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure (redefine the ctrl_config)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    type: str = "Adc"
    ctrl_config : CtrlConfig= CtrlConfig()
    
    cfg: Cfg = Cfg()
    stat: Stat = Stat()
    rpcs: Rpcs = Rpcs()
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    def validate_extra(cls, name, extra, values):
        ctrl = values['ctrl_config']
        if name in ctrl.axes:
            if "cfgfile" in extra:
                axis_io = AxisIoConfig( path=name, **extra )
                # extra = cls.Motor.parse_obj( io.load_config(axis_io.cfgfile)[name] )
                # extra = cls._Motor.parse_obj( io.load_config(axis_io.cfgfile)[name]  )
                extra = axis_io.load()

            else:
                extra = super().validate_extra(name, extra, values)
                if not isinstance(extra, BaseDevice.Config):
                    raise ValueError(f"axis {name} is not a device")
        return extra   
    
    @property
    def motor1(self):
        axis =  self.ctrl_config.axes[0]
        try:
            return self.__dict__[axis]
        except KeyError:
            raise ValueError(f"The axis refered as {axis!r} is not in configuration")
    
    
    @property
    def motor2(self):
        axis =  self.ctrl_config.axes[1]
        try:
            return self.__dict__[axis]
        except KeyError:
            raise ValueError(f"The axis refered as {axis!r} is not in configuration")

    
@record_class(overwrite=True)
class Adc(Base):
    """ ELt Standard Adc device """
    Config = AdcConfig
    Cfg = Cfg
    Stat = Stat
    Rpcs = Rpcs
    
    class Data(Base.Data):
        Cfg = Cfg.Data
        Stat = Stat.Data
        Rpcs = Rpcs.Data
        
        cfg: Cfg = Cfg()
        stat: Stat = Stat()
        rpcs: Rpcs = Rpcs()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #return 
        # at minima we can copy the IP address to the motor if empty 
        self.config.motor1.address = self.config.address
        self.config.motor2.address = self.config.address
        # add set some default prefix if they are empty 
        # using __dict__ here so assignment is not checked 
        if not self.motor1.config.prefix:
            self.motor1.config.__dict__['prefix'] = kjoin( self.config.prefix,"motor1")
        if not self.config.motor2.prefix:
            self.motor2.config.__dict__['prefix'] = kjoin(self.config.prefix, "motor2")
        
    # @property
    # def motor1(self):
    #     return getattr(self, self.config.ctrl_config.axes[0])

    # @property
    # def motor2(self):
    #     return getattr(self, self.config.ctrl_config.axes[1])
        

    @property
    def motors(self) -> list:
        return (self.motor1, self.motor2)
    
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
            
    def get_configuration(self, exclude_unset=True, **kwargs) -> Dict[Base.Node,Any]:
        cfg_dict = {}
        for m in self.motors:
            cfg_dict.update( m.get_configuration(exclude_unset=exclude_unset) )
        
        config = self._config 
        
        ctrl_config = config.ctrl_config
        # just update what is in ctrl_config, except axes      
        cfg_dict.update( {getattr(self.cfg, k):v for k,v in ctrl_config.dict().items() if k not in ["axes"]} ) 
        cfg_dict.update( {getattr(self.cfg, k):v for k,v in  kwargs.items() } )
        return cfg_dict
    
    def init(self) -> Base.Node:
        # fix a feature inside the FB_MA, the RPC_Init return silently zero even if the
        # device is not in the right state
        # TODO remove the patch when this is fixed from ESO side 
        if self.stat.substate.get() != self.SUBSTATE.NOTOP_NOTREADY:
            raise RpcError("Should be in NOTOP_NOTREADY state")
        self.rpcs.rpcInit.rcall()
        return self.stat.is_ready
    
    def stop(self) -> None:
        """ Stop all ADC motions """
        self.rpcs.rpcStop.rcall()
    
    def stop_track(self) -> None:
        self.rpcs.rpcStopTrack.rcall()
        return NegNode(node=self.stat.is_tracking)

    def start_track(self, angle=0.0) -> Base.Node:
        """ Start tracking (AUTO mode)
        
        Args:
            angle (float, optional): target angle default = 0.0
            
        Returns:
            is_tracking:  the :class:`NodeAlias` .stat.is_tracking to check if the device is in tracking  
        """
        self.rpcs.rpcStartTrack.rcall(angle)
        return self.stat.is_tracking
        
    def move_angle(self, angle=0.0) -> Base.Node:
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
        self.rpcs.rpcMoveAngle.rcall(angle)
        return self.stat.is_standstill
        
    def move_abs(self, axis, pos, vel) -> Base.Node:
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
        self.rpcs.rpcMoveAbs.rcall(axis, pos, vel)
        return self.stat.is_standstill
    
    def move_rel(self, axis, pos, vel) -> Base.Node:
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
        self.rpcs.rpcMoveRel.rcall(axis, pos, vel)
        return self.stat.is_standstill

    def move_vel(self, axis, vel) -> Base.Node:
        """ Move one or all motor in velocity 
        
        Args:
            axis (int): 0 for all motors 1 for axis 1 and 2 for axis 2
            vel (float): target velocity 
        
        Return:
           None
        """
        self.rpcs.rpcMoveVel.rcall(axis, vel)
        


if __name__ == "__main__":
    adc = Adc('adc')    
    from pydevmgr_elt import open_elt_device
    
    adc = open_elt_device('tins/adc1.yml', 'adc1')
    print(adc.motor1.config.address)
    
    print("OK")
