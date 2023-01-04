from pydevmgr_core import  NodeVar
from pydevmgr_elt.base import EltDevice,  GROUP

Base = EltDevice.Cfg

N = Base.Node # Base Node
NC = N.Config
NV = NodeVar # used in Data 



class LampCfg(Base):
    class Config(Base.Config):
        analog_range: NC = NC(suffix='cfg.nFullRange', parser='UaUInt32')
        analog_threshold: NC = NC(suffix='cfg.nAnalogThreshold', parser='UaInt32')
        cooldown: NC = NC(suffix='cfg.nCooldown', parser='UaUInt32')
        ignore_fault: NC = NC(suffix='cfg.bIgnoreFault' )
        initial_state: NC = NC(suffix='cfg.bInitialState' )
        initial_intensity: NC = NC(suffix="cfg.lrInitialIntensity")
        invert_analog: NC = NC(suffix='cfg.bInvertAnalog' )
        low_fault: NC = NC(suffix='cfg.bActiveLowFault' )
        low_on: NC = NC(suffix='cfg.bActiveLowOn' )
        low_switch: NC = NC(suffix='cfg.bActiveLowSwitch' )
        maxon: NC = NC(suffix='cfg.nMaxOn', parser='UaUInt32')
        timeout: NC = NC(suffix='cfg.nTimeout', parser='UaUInt32')
        warmup: NC = NC(suffix='cfg.nWarmup', parser='UaUInt32')


    
    class Data(Base.Data):
        analog_range: NV[int] = 0
        analog_threshold: NV[int] = 0
        cooldown: NV[int] = 0
        ignore_fault: NV[bool] = False
        initial_state: NV[bool] = False
        initial_intensity: NV[float] = 0.0
        invert_analog: NV[bool] = False
        low_fault: NV[bool] = False
        low_on: NV[bool] = False
        low_switch: NV[bool] = False
        maxon: NV[int] = 0
        timeout: NV[int] = 0
        warmup: NV[int] = 0
              

