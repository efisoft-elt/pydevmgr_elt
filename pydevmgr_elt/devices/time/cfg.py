from pydevmgr_core import   NodeVar
from pydevmgr_elt.base import EltDevice  

Base = EltDevice.Interface

N = Base.Node # Base Node
NC = N.Config
NV = NodeVar # used in Data 


# Nothing to declare cfg is empty 
class TimeCfg(Base):
    class Config(Base.Config):
        pass    
    class Data(Base.Data):
        pass           

