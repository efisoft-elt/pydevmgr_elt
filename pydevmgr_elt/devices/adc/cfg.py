from pydevmgr_core import    NodeVar
from pydevmgr_elt.base import EltDevice

from enum import Enum
Base = EltDevice.Cfg

N = Base.Node # Base Node
NC = N.Config
NV = NodeVar # used in Data 



class AdcCfg(Base):
    class Config(Base.Config):
        pslope:          NC = NC(suffix="cfg.lrPslope")
        poffset:         NC = NC(suffix="cfg.lrPoffset")
        tslope:          NC = NC(suffix="cfg.lrTslope")
        toffset:         NC = NC(suffix="cfg.lrToffset")
        afactor:         NC = NC(suffix="cfg.lrAfactor")
        zdlimit:         NC = NC(suffix="cfg.lrZDlimit")
        minelev:         NC = NC(suffix="cfg.lrMinElev")
        latitude:        NC = NC(suffix="cfg.site.latitude")
        longitude:       NC = NC(suffix="cfg.site.longitude")
        trk_period:      NC = NC(suffix="cfg.nMinSkipCycles", parser="UaInt32")
        trk_threshold:   NC = NC(suffix="cfg.lrTrkThreshold")
        mot1_signoff:    NC = NC(suffix="cfg.unitCfg[1].nSignOff",parser="UaInt32")
        mot2_signoff:    NC = NC(suffix="cfg.unitCfg[2].nSignOff",parser="UaInt32")
        mot1_signauto:   NC = NC(suffix="cfg.unitCfg[1].nSignAuto",parser="UaInt32")
        mot2_signauto:   NC = NC(suffix="cfg.unitCfg[2].nSignAuto",parser="UaInt32")
        mot1_signphi:    NC = NC(suffix="cfg.unitCfg[1].nSignPhi",parser="UaInt32")
        mot2_signphi:    NC = NC(suffix="cfg.unitCfg[2].nSignPhi",parser="UaInt32")
        mot1_refoff:     NC = NC(suffix="cfg.unitCfg[1].lrRefOff")
        mot2_refoff:     NC = NC(suffix="cfg.unitCfg[2].lrRefOff")
        mot1_refauto:    NC = NC(suffix="cfg.unitCfg[1].lrRefAuto")
        mot2_refauto:    NC = NC(suffix="cfg.unitCfg[2].lrRefAuto")
        mot1_coffset:    NC = NC(suffix="cfg.unitCfg[1].lrCoffset")
        mot2_coffset:    NC = NC(suffix="cfg.unitCfg[2].lrCoffset")
        mot1_poffset:    NC = NC(suffix="cfg.unitCfg[1].lrPosOffset")
        mot2_poffset:    NC = NC(suffix="cfg.unitCfg[2].lrPosOffset")
        mot1_drotfactor: NC = NC(suffix="cfg.unitCfg[1].lrDrotFactor")
        mot2_drotfactor: NC = NC(suffix="cfg.unitCfg[2].lrDrotFactor")
        
    class Data(Base.Data):
        pslope:             NV[float]  =  0.0023
        poffset:            NV[float]  =  743.0
        tslope:             NV[float]  =  -0.0061
        toffset:            NV[float]  =  12.0
        afactor:            NV[float]  =  3.32
        zdlimit:            NV[float]  =  0.0174533
        minelev:            NV[float]  =  27.54
        latitude:           NV[float]  =  -0.429833092
        longitude:          NV[float]  =  1.228800386
        trk_period:         NV[int]  =  0 #cfg.nMinSkipCycles
        trk_threshold:      NV[float]  =  1.0
        mot1_signoff:       NV[int]    =  1
        mot2_signoff:       NV[int]    =  1
        mot1_signauto:      NV[int]    =  1
        mot2_signauto:      NV[int]    =  1
        mot1_signphi:       NV[int]    =  1
        mot2_signphi:       NV[int]    =  1
        mot1_refoff:        NV[float]  =  0.0
        mot2_refoff:        NV[float]  =  0.0
        mot1_refauto:       NV[float]  =  0.0
        mot2_refauto:       NV[float]  =  0.0
        mot1_coffset:       NV[float]  =  0.0
        mot2_coffset:       NV[float]  =  0.0
        mot1_poffset:       NV[float]  =  0.0
        mot2_poffset:       NV[float]  =  0.0
        mot1_drotfactor:    NV[float]  =  0.0
        mot2_drotfactor:    NV[float]  =  0.0

if __name__ == "__main__":
    AdcCfg()
