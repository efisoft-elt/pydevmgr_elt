

from pydevmgr_core import   NodeVar
from pydevmgr_core.base.dataclass import set_data_model
from pydevmgr_elt.base import EltDevice  


Base = EltDevice.Interface

N = Base.Node # Base Node
NC = N.Config
NV = NodeVar # used in Data 


@set_data_model
class AoChannels4(Base):
    class Config:
        ao1:    NC =  NC(suffix="ctrl.arrAO[0].lrValueUser", vtype=float)
        ao2:    NC =  NC(suffix="ctrl.arrAO[1].lrValueUser", vtype=float)
        ao3:    NC =  NC(suffix="ctrl.arrAO[2].lrValueUser", vtype=float)
        ao4:    NC =  NC(suffix="ctrl.arrAO[3].lrValueUser", vtype=float)  

@set_data_model
class AoChannels8(AoChannels4):
    class Config:
        ao5:    NC =  NC(suffix="ctrl.arrAO[4].lrValueUser", vtype=float)
        ao6:    NC =  NC(suffix="ctrl.arrAO[5].lrValueUser", vtype=float)
        ao7:    NC =  NC(suffix="ctrl.arrAO[6].lrValueUser", vtype=float)
        ao8:    NC =  NC(suffix="ctrl.arrAO[7].lrValueUser", vtype=float)

@set_data_model
class AoChannels16(AoChannels8):
    class Config:

        ao9:    NC =  NC(suffix="ctrl.arrAO[8].lrValueUser", vtype=float)
        ao10:   NC =  NC(suffix="ctrl.arrAO[9].lrValueUser", vtype=float)
        ao11:   NC =  NC(suffix="ctrl.arrAO[10].lrValueUser", vtype=float)
        ao12:   NC =  NC(suffix="ctrl.arrAO[11].lrValueUser", vtype=float)
        ao13:   NC =  NC(suffix="ctrl.arrAO[12].lrValueUser", vtype=float)
        ao14:   NC =  NC(suffix="ctrl.arrAO[13].lrValueUser", vtype=float)
        ao15:   NC =  NC(suffix="ctrl.arrAO[14].lrValueUser", vtype=float)
        ao16:   NC =  NC(suffix="ctrl.arrAO[15].lrValueUser", vtype=float)

@set_data_model
class AoChannels32(AoChannels16):
    class Config:
        ao17:   NC =  NC(suffix="ctrl.arrAO[16].lrValueUser", vtype=float)
        ao18:   NC =  NC(suffix="ctrl.arrAO[17].lrValueUser", vtype=float)
        ao19:   NC =  NC(suffix="ctrl.arrAO[18].lrValueUser", vtype=float)
        ao20:   NC =  NC(suffix="ctrl.arrAO[19].lrValueUser", vtype=float)
        ao21:   NC =  NC(suffix="ctrl.arrAO[20].lrValueUser", vtype=float)
        ao22:   NC =  NC(suffix="ctrl.arrAO[21].lrValueUser", vtype=float)
        ao23:   NC =  NC(suffix="ctrl.arrAO[22].lrValueUser", vtype=float)
        ao24:   NC =  NC(suffix="ctrl.arrAO[23].lrValueUser", vtype=float)
        ao25:   NC =  NC(suffix="ctrl.arrAO[24].lrValueUser", vtype=float)
        ao26:   NC =  NC(suffix="ctrl.arrAO[25].lrValueUser", vtype=float)
        ao27:   NC =  NC(suffix="ctrl.arrAO[26].lrValueUser", vtype=float)
        ao28:   NC =  NC(suffix="ctrl.arrAO[27].lrValueUser", vtype=float)
        ao29:   NC =  NC(suffix="ctrl.arrAO[28].lrValueUser", vtype=float)
        ao30:   NC =  NC(suffix="ctrl.arrAO[29].lrValueUser", vtype=float)
        ao31:   NC =  NC(suffix="ctrl.arrAO[30].lrValueUser", vtype=float)
        ao32:   NC =  NC(suffix="ctrl.arrAO[31].lrValueUser", vtype=float)

