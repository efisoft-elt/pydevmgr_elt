from enum import Enum
import weakref
from pydevmgr_core.base.base import ParentWeakRef
from pydevmgr_core.base.node_alias import BaseNodeAlias1 

class ChanelType(str, Enum):
    DI = 'DI'
    AI = 'AI'
    II = 'II'

ChanelType.DI.groupMap = "diChannels"
ChanelType.AI.groupMap = "aiChannels"
ChanelType.II.groupMap = "iiChannels"


class SensorChannelAlias(ParentWeakRef, BaseNodeAlias1):
    # class Config(BaseNodeAlias1.Config):
    class Config:
        name: str 
        map: str 
        description: str = ""
        alias: str = ""
        header: bool = False
        log: bool = False
        fits_prefix: str = ""
        type: ChanelType = ChanelType.DI
        unit: str = ""
    
    def nodes(self):
        channels = getattr( self.get_parent(), ChanelType(self.config.type).groupMap)
        yield getattr( channels, self.config.map )

if __name__ is "__main__":
    SensorChannelAlias()
        
