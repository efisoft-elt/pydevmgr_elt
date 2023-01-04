from pydevmgr_core import   NodeVar
from pydevmgr_elt.base import EltDevice

Base = EltDevice.Cfg

N = Base.Node # Base Node
NC = N.Config
NV = NodeVar # used in Data 


class ShutterCfg(Base):
    class Config(Base.Config):
        ignore_closed: NC = NC(suffix='cfg.bIgnoreClosed' )
        ignore_fault: NC = NC(suffix='cfg.bIgnoreFault' )
        ignore_open: NC = NC(suffix='cfg.bIgnoreOpen' )
        initial_state: NC = NC(suffix='cfg.bInitialState' )
        low_closed: NC = NC(suffix='cfg.bActiveLowClosed' )
        low_fault: NC = NC(suffix='cfg.bActiveLowFault' )
        low_open: NC = NC(suffix='cfg.bActiveLowOpen' )
        low_switch: NC = NC(suffix='cfg.bActiveLowSwitch' )
        timeout: NC = NC(suffix='cfg.nTimeout', parser='UaUInt32')

    
    class Data(Base.Data):
        ignore_closed: NV[bool] = False
        ignore_fault: NV[bool] = False
        ignore_open: NV[bool] = False
        initial_state: NV[bool] = False
        low_closed: NV[bool] = False
        low_fault: NV[bool] = False
        low_open: NV[bool] = False
        low_switch: NV[bool] = False
        timeout: NV[int] = 3000

           

