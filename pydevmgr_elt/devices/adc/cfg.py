from pydevmgr_core import    NodeVar
from pydevmgr_core.base.dataclass import set_data_model
from pydevmgr_elt.base import EltDevice

from enum import Enum
Base = EltDevice.Cfg

N = Base.Node # Base Node
NC = N.Config
NV = NodeVar # used in Data 


@set_data_model
class AdcCfg(Base):
    class Config(Base.Config):
        pslope:           NC  =  NC(suffix="cfg.lrPslope",                 vtype=(float, 0.0023))
        poffset:          NC  =  NC(suffix="cfg.lrPoffset",                vtype=(float, 743.0))
        tslope:           NC  =  NC(suffix="cfg.lrTslope",                 vtype=(float, -0.0061))
        toffset:          NC  =  NC(suffix="cfg.lrToffset",                vtype=(float, 12.0))
        afactor:          NC  =  NC(suffix="cfg.lrAfactor",                vtype=(float, 3.32))
        zdlimit:          NC  =  NC(suffix="cfg.lrZDlimit",                vtype=(float,0.0174533) )
        minelev:          NC  =  NC(suffix="cfg.lrMinElev",                vtype=(float, 27.54))
        latitude:         NC  =  NC(suffix="cfg.site.latitude",            vtype=(float, -0.429833092))
        longitude:        NC  =  NC(suffix="cfg.site.longitude",           vtype=(float, -1.228800386))
        trk_period:       NC  =  NC(suffix="cfg.nMinSkipCycles",           vtype=int,   parser="UaInt32")
        trk_threshold:    NC  =  NC(suffix="cfg.lrTrkThreshold",           vtype=(float, 1.0))
        mot1_signoff:     NC  =  NC(suffix="cfg.unitCfg[1].nSignOff",      vtype=(int,1),  parser="UaInt32")
        mot2_signoff:     NC  =  NC(suffix="cfg.unitCfg[2].nSignOff",      vtype=(int,1),  parser="UaInt32")
        mot1_signauto:    NC  =  NC(suffix="cfg.unitCfg[1].nSignAuto",     vtype=(int,1),  parser="UaInt32")
        mot2_signauto:    NC  =  NC(suffix="cfg.unitCfg[2].nSignAuto",     vtype=(int,1),  parser="UaInt32")
        mot1_signphi:     NC  =  NC(suffix="cfg.unitCfg[1].nSignPhi",      vtype=(int,1),  parser="UaInt32")
        mot2_signphi:     NC  =  NC(suffix="cfg.unitCfg[2].nSignPhi",      vtype=(int,1),  parser="UaInt32")
        mot1_refoff:      NC  =  NC(suffix="cfg.unitCfg[1].lrRefOff",      vtype=float)
        mot2_refoff:      NC  =  NC(suffix="cfg.unitCfg[2].lrRefOff",      vtype=float)
        mot1_refauto:     NC  =  NC(suffix="cfg.unitCfg[1].lrRefAuto",     vtype=float)
        mot2_refauto:     NC  =  NC(suffix="cfg.unitCfg[2].lrRefAuto",     vtype=float)
        mot1_coffset:     NC  =  NC(suffix="cfg.unitCfg[1].lrCoffset",     vtype=float)
        mot2_coffset:     NC  =  NC(suffix="cfg.unitCfg[2].lrCoffset",     vtype=float)
        mot1_poffset:     NC  =  NC(suffix="cfg.unitCfg[1].lrPosOffset",   vtype=float)
        mot2_poffset:     NC  =  NC(suffix="cfg.unitCfg[2].lrPosOffset",   vtype=float)
        mot1_drotfactor:  NC  =  NC(suffix="cfg.unitCfg[1].lrDrotFactor",  vtype=float)
        mot2_drotfactor:  NC  =  NC(suffix="cfg.unitCfg[2].lrDrotFactor",  vtype=float)
        


if __name__ == "__main__":
    AdcCfg()
