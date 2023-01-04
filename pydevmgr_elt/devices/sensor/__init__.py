from pydantic.main import BaseModel
from pydevmgr_elt.devices.sensor.stat import SensorStat as Stat
from pydevmgr_elt.devices.sensor.cfg  import SensorCfg as Cfg
from pydevmgr_elt.devices.sensor.rpcs import SensorRpcs as Rpcs


from pydevmgr_elt.devices.sensor.aiChannels import AiChannels32, AiChannels16, AiChannels8, AiChannels4     
from pydevmgr_elt.devices.sensor.aoChannels import AoChannels32 , AoChannels16, AoChannels8, AoChannels4   
from pydevmgr_elt.devices.sensor.diChannels import DiChannels32 , DiChannels16, DiChannels8, DiChannels4   
from pydevmgr_elt.devices.sensor.doChannels import DoChannels32, DoChannels16, DoChannels8, DoChannels4   

from pydevmgr_elt.devices.sensor.channel import  SensorChannelAlias

from pydevmgr_elt.base import EltDevice, register
from typing import List, Optional

Base = EltDevice




class SensorCtrlConfig(Base.Config.CtrlConfig):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure (on top of CtrlConfig)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    timeout:          int  = 2000 

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
class BaseSensorConfig(Base.Config):
    CtrlConfig = SensorCtrlConfig
    
    Cfg = Cfg.Config
    Stat = Stat.Config
    Rpcs = Rpcs.Config

      
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure (redefine the ctrl_config)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    type: str = "BaseSensor"
    ctrl_config : CtrlConfig= CtrlConfig()
    
    channels: List[SensorChannelAlias.Config] = []

    cfg: Cfg = Cfg()
    stat: Stat = Stat()
    rpcs: Rpcs = Rpcs()
     
      
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class BaseSensor(Base):
    """ ELt Standard Sensor device """
    Config = BaseSensorConfig
    
    Cfg = Cfg
    Stat = Stat
    Rpcs = Rpcs
    
    ChannelAlias = SensorChannelAlias
    

    class Data(Base.Data):
        Cfg = Cfg.Data
        Stat = Stat.Data
        Rpcs = Rpcs.Data
        
        cfg: Cfg = Cfg()
        stat: Stat = Stat()
        rpcs: Rpcs = Rpcs()
 
@register
class Sensor(BaseSensor):
    class Config:
        type: str = "Sensor"
        AiChannels = AiChannels32.Config
        AoChannels = AoChannels32.Config
        DiChannels = DiChannels32.Config
        DoChannels = DoChannels32.Config
        aiChannels: AiChannels = AiChannels()
        aoChannels: AoChannels = AoChannels()
        diChannels: DiChannels = DiChannels()
        doChannels: DoChannels = DoChannels()

    AiChannels = AiChannels32
    AoChannels = AoChannels32
    DiChannels = DiChannels32
    DoChannels = DoChannels32




@register
class Sensor8_4(BaseSensor):
    class Config:
        type: str = "Sensor8_4"
        DiChannels = DiChannels8.Config
        AiChannels = AiChannels4.Config
        aiChannels: AiChannels = AiChannels()
        diChannels: DiChannels = DiChannels()

    DiChannels = DiChannels8
    AiChannels = AiChannels4

        

if __name__ == "__main__":
    Sensor()
