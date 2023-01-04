from pydevmgr_core import  NodeVar
from pydevmgr_elt.base import EltDevice
from enum import Enum
Base = EltDevice.Interface

N = Base.Node # Base Node
NC = N.Config
NV = NodeVar # used in Data 



class CcsSimCfg(Base):
    class Config(Base.Config):
        latitude: NC = NC(suffix="cfg.site.latitude")
        longitude: NC = NC(suffix="cfg.site.longitude")
        height: NC = NC(suffix="cfg.site.height")

    class Data(Base.Data):
        latitude:  NodeVar[float] =  -0.429833092     
        longitude:  NodeVar[float] = 1.228800386    
        height: NodeVar[float] = 3046.0

