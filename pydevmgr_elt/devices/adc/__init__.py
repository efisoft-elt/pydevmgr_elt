from pydevmgr_elt.devices.adc.stat import AdcStat as Stat
from pydevmgr_elt.devices.adc.cfg  import AdcCfg as Cfg
from pydevmgr_elt.devices.adc.rpcs import AdcRpcs as Rpcs

from pydevmgr_elt.base import EltDevice
from pydevmgr_core import record_class, Defaults, RpcError, ksplit
from typing import Optional, Any, Dict, List
from pydevmgr_elt.devices.motor import Motor
from pydevmgr_elt import io
from pydantic import BaseModel 

Base = EltDevice


class AxisIoConfig(BaseModel):
    """ Configuration for one Axis """
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    prefix  : str = ""
    cfgfile : str = ""
    

class AdcCtrlConfig(Base.Config.CtrlConfig):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure (on top of CtrlConfig)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    latitude  : Optional[float] = -0.429833092 
    longitude : Optional[float] = 1.228800386
    axes : List[str] = [] # name of axes 

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
class AdcConfig(Base.Config):
    Ctrl = AdcCtrlConfig
    
    Cfg = Cfg.Config
    Stat = Stat.Config
    Rpcs = Rpcs.Config
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure (redefine the ctrl_config)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    type: str = "Adc"
    ctrl_config : Ctrl= Ctrl()
    
    cfg: Cfg = Cfg()
    stat: Stat = Stat()
    rpcs: Rpcs = Rpcs()
    
    # Add the motors here 
    motor1: Defaults[Motor.Config] = Motor.Config()
    motor2: Defaults[Motor.Config] = Motor.Config()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    @classmethod
    def from_cfgdict(cls, d):
        if d.get("version", None)=="pydevmgr":
            return cls.parse_obj(d)
        # patch to be copatible with ESO config files 
        ctrl = cls.Ctrl.parse_obj ( d.get('ctrl_config', {}))
        if ctrl.axes:
            axis1, axis2 = ctrl.axes
            axis1_io = AxisIoConfig(**d[axis1])
            axis2_io = AxisIoConfig(**d[axis2])
            # d['motor1'] = io.load_config(axis1_io.cfgfile)[axis1_io.prefix]
            # d['motor2'] = io.load_config(axis2_io.cfgfile)[axis2_io.prefix]
            # seems that it the rules that the name in this file is the name in the 
            # motor config file 
            d['motor1'] = io.load_config(axis1_io.cfgfile)[axis1]
            d['motor2'] = io.load_config(axis2_io.cfgfile)[axis2]



            del d[axis1]
            del d[axis2]    
        return d

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
        # at minima we can copy the IP address to the motor if empty 
        self.config.motor1.address = self.config.address
        self.config.motor2.address = self.config.address
        # add set some default prefix if they are empty 
        if not self.config.motor1.prefix:
            self.config.motor1.prefix = ksplit( self.config.prefix,"motor1")
        if not self.config.motor2.prefix:
            self.config.motor2.prefix = ksplit(self.config.prefix, "motor2")

        

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
        cfg_dict.update( {self.cfg.get_node(k):v for k,v in ctrl_config.dict().items() if k not in ["axes"]} ) 
        cfg_dict.update( {self.cfg.get_node(k):v for k,v in  kwargs.items() } )
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
