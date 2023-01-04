

from pydevmgr_core import   NodeVar
from pydevmgr_elt.base import EltDevice  


Base = EltDevice.Interface

N = Base.Node # Base Node
NC = N.Config
NV = NodeVar # used in Data 



class AoChannels4(Base):
    class Config:
        ao1:    NC =  NC(suffix="ctrl.arrAO[0].lrValueUser")
        ao2:    NC =  NC(suffix="ctrl.arrAO[1].lrValueUser")
        ao3:    NC =  NC(suffix="ctrl.arrAO[2].lrValueUser")
        ao4:    NC =  NC(suffix="ctrl.arrAO[3].lrValueUser")  


class AoChannels8(AoChannels4):
    class Config:
        ao5:    NC =  NC(suffix="ctrl.arrAO[4].lrValueUser")
        ao6:    NC =  NC(suffix="ctrl.arrAO[5].lrValueUser")
        ao7:    NC =  NC(suffix="ctrl.arrAO[6].lrValueUser")
        ao8:    NC =  NC(suffix="ctrl.arrAO[7].lrValueUser")
    
class AoChannels16(AoChannels8):
    class Config:

        ao9:    NC =  NC(suffix="ctrl.arrAO[8].lrValueUser")
        ao10:   NC =  NC(suffix="ctrl.arrAO[9].lrValueUser")
        ao11:   NC =  NC(suffix="ctrl.arrAO[10].lrValueUser")
        ao12:   NC =  NC(suffix="ctrl.arrAO[11].lrValueUser")
        ao13:   NC =  NC(suffix="ctrl.arrAO[12].lrValueUser")
        ao14:   NC =  NC(suffix="ctrl.arrAO[13].lrValueUser")
        ao15:   NC =  NC(suffix="ctrl.arrAO[14].lrValueUser")
        ao16:   NC =  NC(suffix="ctrl.arrAO[15].lrValueUser")

class AoChannels32(AoChannels16):
    class Config:
        ao17:   NC =  NC(suffix="ctrl.arrAO[16].lrValueUser")
        ao18:   NC =  NC(suffix="ctrl.arrAO[17].lrValueUser")
        ao19:   NC =  NC(suffix="ctrl.arrAO[18].lrValueUser")
        ao20:   NC =  NC(suffix="ctrl.arrAO[19].lrValueUser")
        ao21:   NC =  NC(suffix="ctrl.arrAO[20].lrValueUser")
        ao22:   NC =  NC(suffix="ctrl.arrAO[21].lrValueUser")
        ao23:   NC =  NC(suffix="ctrl.arrAO[22].lrValueUser")
        ao24:   NC =  NC(suffix="ctrl.arrAO[23].lrValueUser")
        ao25:   NC =  NC(suffix="ctrl.arrAO[24].lrValueUser")
        ao26:   NC =  NC(suffix="ctrl.arrAO[25].lrValueUser")
        ao27:   NC =  NC(suffix="ctrl.arrAO[26].lrValueUser")
        ao28:   NC =  NC(suffix="ctrl.arrAO[27].lrValueUser")
        ao29:   NC =  NC(suffix="ctrl.arrAO[28].lrValueUser")
        ao30:   NC =  NC(suffix="ctrl.arrAO[29].lrValueUser")
        ao31:   NC =  NC(suffix="ctrl.arrAO[30].lrValueUser")
        ao32:   NC =  NC(suffix="ctrl.arrAO[31].lrValueUser")

