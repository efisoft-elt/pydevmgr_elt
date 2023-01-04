from pydevmgr_core import  NodeVar
from pydevmgr_elt.base import EltDevice

Base = EltDevice.Cfg

N = Base.Node # Base Node
NC = N.Config
NV = NodeVar # used in Data 



class SensorCfg(Base):
    class Config(Base.Config):
        pass 
    
    class Data(Base.Data):
        pass     
