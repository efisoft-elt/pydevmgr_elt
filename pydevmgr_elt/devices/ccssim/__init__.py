from .stat import CcsSimStat as Stat
from .cfg  import CcsSimCfg as Cfg
from .rpcs import CcsSimRpcs as Rpcs
from .ctrl import CcsSimCtrl as Ctrl

from pydevmgr_elt.base import EltDevice
from pydevmgr_core import record_class, upload
from typing import Optional


Base = EltDevice


class CcsSimCtrlConfig(Base.Config.CtrlConfig):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure (on top of CtrlConfig)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    latitude  : Optional[float] = -0.429833092 
    longitude : Optional[float] = 1.228800386
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
class CcsSimConfig(Base.Config):
    CtrlConf = CcsSimCtrlConfig
    

    Cfg = Cfg.Config
    Stat = Stat.Config
    Rpcs = Rpcs.Config
    Ctrl = Ctrl.Config
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure (redefine the ctrl_config)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    type: str = "CcsSim"
    ctrl_config : CtrlConf= CtrlConf()
    
    cfg: Cfg = Cfg()
    stat: Stat = Stat()
    rpcs: Rpcs = Rpcs()
    ctrl : Ctrl = Ctrl()
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



@record_class
class CcsSim(Base):
    """ ELt Standard CcsSim device  as in IFW v3.0 (this may change)"""
    Config = CcsSimConfig
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

    def reset(self) -> None:
        """ Do nothing for CcsSim (here for compatibility) """
        pass

    def enable(self) -> None:
        """Do Nothing for CcsSim (here for compatibility) """
        pass

    def disable(self) -> None:
        """ Do nothing for CcsSim (here for compatibility) """
        pass

    def init(self) -> None:
        """ Do Nothing for CcsSim (here for compatibility)  """
    
    def set_coordinates(self, ra: float, dec: float, equinox: float = 2000.0) -> None:
        """ Set coordinates in CcsSim 

        Args:
            ra (float): hhmmss.xxx
            dec (float): ddmmss.xxx
            equinox (float, optional): Default is 2000  
        """
        self.rpc.rpcSetCoordinates.rcall(ra, dec, equinox)
    
    def set_environment(self, 
            temperature: Optional[float] = None, 
            pressure: Optional[float] =None, 
            humidity: Optional[float] =None, 
            lapserate: Optional[float] =None, 
            wavelength: Optional[float] = None, 
            dut: Optional[float] = None                              
        ):
        """ set environmnent data to the Ccs Simulator 
        
        Each settings arguments are potionals: 
        temperature, pressure, humidity, lapserate, wavelength, dut
        They are taken into account if not None
        
        """
        nodes = {}
        if temperature is not None:
            nodes[self.ctrl.temperature] = temperature
        
        if pressure is not None:
            nodes[self.ctrl.pressure] = pressure
        
        if humidity is not None:
            nodes[self.ctrl.humidity] = humidity
            
        if lapserate is not None:
            nodes[self.ctrl.lapserate] = lapserate    
        
        if wavelength is not None:
            nodes[self.ctrl.wavelength] = wavelength 
        
        if dut is not None:
            nodes[self.ctrl.dut] = dut        
        upload(nodes)          
        
   

