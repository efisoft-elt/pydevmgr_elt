from pydevmgr_core import   NodeVar
from pydevmgr_core.base.dataclass import set_data_model
from pydevmgr_elt.base import EltDevice

Base = EltDevice.Cfg

N = Base.Node # Base Node
NC = N.Config
NV = NodeVar # used in Data 

@set_data_model
class ShutterCfg(Base):
    class Config(Base.Config):
        ignore_closed:  NC  =  NC(suffix='cfg.bIgnoreClosed'     , vtype=bool)
        ignore_fault:   NC  =  NC(suffix='cfg.bIgnoreFault'      , vtype=bool)
        ignore_open:    NC  =  NC(suffix='cfg.bIgnoreOpen'       , vtype=bool)
        initial_state:  NC  =  NC(suffix='cfg.bInitialState'     , vtype=bool)
        low_closed:     NC  =  NC(suffix='cfg.bActiveLowClosed'  , vtype=bool)
        low_fault:      NC  =  NC(suffix='cfg.bActiveLowFault'   , vtype=bool)
        low_open:       NC  =  NC(suffix='cfg.bActiveLowOpen'    , vtype=bool)
        low_switch:     NC  =  NC(suffix='cfg.bActiveLowSwitch'  , vtype=bool)
        timeout:        NC  =  NC(suffix='cfg.nTimeout', vtype=int,  parser='UaUInt32')
    

