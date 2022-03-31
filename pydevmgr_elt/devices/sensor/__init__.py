from pydevmgr_elt.devices.sensor.stat import SensorStat as Stat
from pydevmgr_elt.devices.sensor.cfg  import SensorCfg as Cfg
from pydevmgr_elt.devices.sensor.rpcs import SensorRpcs as Rpcs


from pydevmgr_elt.devices.sensor.aiChannels import AiChannels  
from pydevmgr_elt.devices.sensor.aoChannels import AoChannels  
from pydevmgr_elt.devices.sensor.diChannels import DiChannels  
from pydevmgr_elt.devices.sensor.doChannels import DoChannels  


from pydevmgr_elt.base import EltDevice
from pydevmgr_core import record_class
from typing import Optional

Base = EltDevice


class SensorCtrlConfig(Base.Config.CtrlConfig):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure (on top of CtrlConfig)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    timeout:          int  = 2000 

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
class SensorConfig(Base.Config):
    CtrlConfig = SensorCtrlConfig
    
    Cfg = Cfg.Config
    Stat = Stat.Config
    Rpcs = Rpcs.Config

    AiChannels = AiChannels.Config
    AoChannels = AoChannels.Config
    DiChannels = DiChannels.Config
    DoChannels = DoChannels.Config
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure (redefine the ctrl_config)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    type: str = "Sensor"
    ctrl_config : CtrlConfig= CtrlConfig()
    
    cfg: Cfg = Cfg()
    stat: Stat = Stat()
    rpcs: Rpcs = Rpcs()
    
    aiChannels: AiChannels = AiChannels()
    aoChannels: AoChannels = AoChannels()
    diChannels: DiChannels = DiChannels()
    doChannels: DoChannels = DoChannels()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


@record_class
class Sensor(Base):
    """ ELt Standard Sensor device """
    Config = SensorConfig
    Cfg = Cfg
    Stat = Stat
    Rpcs = Rpcs
    
    AiChannels = AiChannels
    AoChannels = AoChannels
    DiChannels = DiChannels
    DoChannels = DoChannels



    class Data(Base.Data):
        Cfg = Cfg.Data
        Stat = Stat.Data
        Rpcs = Rpcs.Data
        
        cfg: Cfg = Cfg()
        stat: Stat = Stat()
        rpcs: Rpcs = Rpcs()
    
 

if __name__ == "__main__":
    Sensor()
