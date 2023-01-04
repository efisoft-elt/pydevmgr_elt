
from pydevmgr_core import    NodeVar
from pydevmgr_elt.base import EltDevice


Base = EltDevice.Interface

N = Base.Node # Base Node
NC = N.Config
NV = NodeVar # used in Data 




class DoChannels4(Base):
    class Config(Base.Config):
        do1:   NC =   NC(suffix="ctrl.arrDO[0].bValue")
        do2:   NC =   NC(suffix="ctrl.arrDO[1].bValue")
        do3:   NC =   NC(suffix="ctrl.arrDO[2].bValue")
        do4:   NC =   NC(suffix="ctrl.arrDO[3].bValue") 

class DoChannels8(DoChannels4):
    class Config:
        do5:    NC =  NC(suffix="ctrl.arrDO[4].bValue")
        do6:    NC =  NC(suffix="ctrl.arrDO[5].bValue")
        do7:    NC =  NC(suffix="ctrl.arrDO[6].bValue")
        do8:    NC =  NC(suffix="ctrl.arrDO[7].bValue")

class DoChannels16(DoChannels8):
    class Config:
        do9:    NC =  NC(suffix="ctrl.arrDO[8].bValue")
        do10:   NC =  NC(suffix="ctrl.arrDO[9].bValue")
        do11:   NC =  NC(suffix="ctrl.arrDO[10].bValue")
        do12:   NC =  NC(suffix="ctrl.arrDO[11].bValue")
        do13:   NC =  NC(suffix="ctrl.arrDO[12].bValue")
        do14:   NC =  NC(suffix="ctrl.arrDO[13].bValue")
        do15:   NC =  NC(suffix="ctrl.arrDO[14].bValue")
        do16:   NC =  NC(suffix="ctrl.arrDO[15].bValue")

class DoChannels32(DoChannels16):
    class Config:
        do17:   NC =  NC(suffix="ctrl.arrDO[16].bValue")
        do18:   NC =  NC(suffix="ctrl.arrDO[17].bValue")
        do19:   NC =  NC(suffix="ctrl.arrDO[18].bValue")
        do20:   NC =  NC(suffix="ctrl.arrDO[19].bValue")
        do21:   NC =  NC(suffix="ctrl.arrDO[20].bValue")
        do22:   NC =  NC(suffix="ctrl.arrDO[21].bValue")
        do23:   NC =  NC(suffix="ctrl.arrDO[22].bValue")
        do24:   NC =  NC(suffix="ctrl.arrDO[23].bValue")
        do25:   NC =  NC(suffix="ctrl.arrDO[24].bValue")
        do26:   NC =  NC(suffix="ctrl.arrDO[25].bValue")
        do27:   NC =  NC(suffix="ctrl.arrDO[26].bValue")
        do28:   NC =  NC(suffix="ctrl.arrDO[27].bValue")
        do29:   NC =  NC(suffix="ctrl.arrDO[28].bValue")
        do30:   NC =  NC(suffix="ctrl.arrDO[29].bValue")
        do31:   NC =  NC(suffix="ctrl.arrDO[30].bValue")
        do32:   NC =  NC(suffix="ctrl.arrDO[31].bValue")








