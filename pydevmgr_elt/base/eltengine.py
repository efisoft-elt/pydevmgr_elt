from dataclasses import dataclass 
from pydevmgr_ua import UaNode, UaDevice, UaRpc
from pydevmgr_core import BaseManager

from .tools import fjoin 



def finalyse_engine(engine, parent, config):
    try:
        fits_prefix = parent.fits_prefix
    except AttributeError:
        fits_prefix = ""
        
    engine.fits_prefix =  fjoin( fits_prefix, getattr(config, "fits_prefix" , ""))

class BaseEltEngine:
    @classmethod
    def new(cls, com, config):
        if config is None:
            config = cls.Config()

        engine = super().new(com, config)
        finalyse_engine(engine, com, config)
        return engine 
 

@dataclass
class EltNodeEngine(BaseEltEngine, UaNode.Engine):
    fits_prefix: str = ""
    class Config(UaNode.Engine.Config):
        fits_prefix: str = ""

@dataclass
class EltRpcEngine(BaseEltEngine, UaRpc.Engine):
    fits_prefix: str = ""
    class Config(UaRpc.Engine.Config):
        fits_prefix: str = ""
                 
@dataclass
class EltEngine(BaseEltEngine, UaDevice.Engine):
    fits_prefix: str = ""
    class Config(UaDevice.Engine.Config):
        fits_prefix: str = ""

@dataclass
class EltManagerEngine(BaseEltEngine, BaseManager.Engine):
    fits_prefix: str = ""
    class Config(BaseManager.Engine.Config):
        fits_prefix: str = ""


 
 
