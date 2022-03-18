from pydevmgr_core import   Defaults, NodeVar
from pydevmgr_elt.devices.motor import Motor
Base = Motor.Cfg


N = Base.Node # Base Node
NC = N.Config
ND = Defaults[NC] # this typing var says that it is a Node object holding default values 
NV = NodeVar # used in Data 



class DrotCfg(Base):
    class Config(Base.Config):
        dir_sign: ND = NC(suffix='cfg.nDirSign', parser='UaInt32')
        focus_sign: ND = NC(suffix='cfg.nFocusSign', parser='UaInt32')
        trk_period: ND = NC(suffix='cfg.nMinSkipCycles', parser='UaInt32')
        
    class Data(Base.Data):
        dir_sign: NV[int] = 0
        focus_sign: NV[int] = 0
        trk_period: NV[int] = 0

