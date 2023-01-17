from pydevmgr_core import  NodeVar
from pydevmgr_core.base.dataclass import set_data_model
from pydevmgr_elt.base import EltDevice
from enum import Enum
Base = EltDevice.Interface

N = Base.Node # Base Node
NC = N.Config
NV = NodeVar # used in Data 


@set_data_model
class CcsSimCfg(Base):
    class Config(Base.Config):
        latitude: NC = NC(suffix="cfg.site.latitude", vtype=(float,-0.429833092))
        longitude: NC = NC(suffix="cfg.site.longitude", vtype=(float, 1.228800386))
        height: NC = NC(suffix="cfg.site.height", vtype=(float,3046.0 ))


