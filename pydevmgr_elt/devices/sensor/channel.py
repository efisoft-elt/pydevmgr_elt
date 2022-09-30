from enum import Enum
from pydantic import BaseModel
import pydevmgr_core 
from pydevmgr_elt.base import EltNode
from pydevmgr_core.nodes import NodeAlias1
from pydevmgr_core import BaseFactory 

class ChanelType(str, Enum):
    DI = 'DI'
    AI = 'AI'
    II = 'II'

ChanelType.DI.groupMap = "diChannels"
ChanelType.AI.groupMap = "aiChannels"
ChanelType.II.groupMap = "iiChannels"


class SensorChannelFactory(BaseFactory):
    name: str
    map: str
    description: str = ""
    alias: str = ""
    header: bool = False
    log: bool = False
    fits_prefix: str = ""
    type: ChanelType = ChanelType.DI
    unit: str = ""
    
    def build(self, parent, name=None):
        
        node_name = ChanelType(self.type).groupMap+"."+self.map
         
        
        config = SensorChannelNodeAlias.Config(
                node = node_name, 
                **self.dict(exclude=set(['type', 'map']), exclude_unset=True ), 
                channel_type = self.type
                )

        return config.build(parent, name or self.name)
         


class SensorChannelNodeAlias(NodeAlias1):
    class Config(NodeAlias1.Config):
        type: str = "SensorChannel"
        name: str = ""
        channel_type: ChanelType = ChanelType.DI
        description: str = ""
        alias: str = ""
        header: bool = False
        log: bool = False
        fits_prefix: str = ""
        type: ChanelType = ChanelType.DI
        unit: str = ""

    


    
    
