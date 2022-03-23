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

        stat_ref:           ND = NC(suffix="cfg.lrStatRef", parser=float)
        sky_ref:            ND = NC(suffix="cfg.lrSkyRef", parser=float)
        elev_ref:           ND = NC(suffix="cfg.lrElevRef", parser=float)
        user_ref:           ND = NC(suffix="cfg.lrUserRef", parser=float)
        user_par1:          ND = NC(suffix="cfg.lrUserPar1", parser=float)
        user_par2:          ND = NC(suffix="cfg.lrUserPar2", parser=float)
        user_par3:          ND = NC(suffix="cfg.lrUserPar3", parser=float)
        user_par4:          ND = NC(suffix="cfg.lrUserPar4", parser=float)
        latitude:           ND = NC(suffix="cfg.site.latitude", parser=float)
        longitude:          ND = NC(suffix="cfg.site.longitude", parser=float) 
        trk_threshold:      ND = NC(suffix="cfg.lrTrkThreshold", parser=float)

   


    class Data(Base.Data):
        dir_sign: NV[int] = 0
        focus_sign: NV[int] = 0
        trk_period: NV[int] = 0

