
from pydevmgr_core import    NodeVar
from pydevmgr_core.base.dataclass import set_data_model
from pydevmgr_elt.base import EltDevice


Base = EltDevice.Interface

N = Base.Node # Base Node
NC = N.Config
NV = NodeVar # used in Data 



@set_data_model
class DoChannels4(Base):
    class Config(Base.Config):
        do1:   NC =   NC(suffix="ctrl.arrDO[0].bValue", vtype=bool)
        do2:   NC =   NC(suffix="ctrl.arrDO[1].bValue", vtype=bool)
        do3:   NC =   NC(suffix="ctrl.arrDO[2].bValue", vtype=bool)
        do4:   NC =   NC(suffix="ctrl.arrDO[3].bValue", vtype=bool) 

@set_data_model
class DoChannels8(DoChannels4):
    class Config:
        do5:    NC =  NC(suffix="ctrl.arrDO[4].bValue", vtype=bool)
        do6:    NC =  NC(suffix="ctrl.arrDO[5].bValue", vtype=bool)
        do7:    NC =  NC(suffix="ctrl.arrDO[6].bValue", vtype=bool)
        do8:    NC =  NC(suffix="ctrl.arrDO[7].bValue", vtype=bool)

@set_data_model
class DoChannels16(DoChannels8):
    class Config:
        do9:    NC =  NC(suffix="ctrl.arrDO[8].bValue", vtype=bool)
        do10:   NC =  NC(suffix="ctrl.arrDO[9].bValue", vtype=bool)
        do11:   NC =  NC(suffix="ctrl.arrDO[10].bValue", vtype=bool)
        do12:   NC =  NC(suffix="ctrl.arrDO[11].bValue", vtype=bool)
        do13:   NC =  NC(suffix="ctrl.arrDO[12].bValue", vtype=bool)
        do14:   NC =  NC(suffix="ctrl.arrDO[13].bValue", vtype=bool)
        do15:   NC =  NC(suffix="ctrl.arrDO[14].bValue", vtype=bool)
        do16:   NC =  NC(suffix="ctrl.arrDO[15].bValue", vtype=bool)

@set_data_model
class DoChannels32(DoChannels16):
    class Config:
        do17:   NC =  NC(suffix="ctrl.arrDO[16].bValue", vtype=bool)
        do18:   NC =  NC(suffix="ctrl.arrDO[17].bValue", vtype=bool)
        do19:   NC =  NC(suffix="ctrl.arrDO[18].bValue", vtype=bool)
        do20:   NC =  NC(suffix="ctrl.arrDO[19].bValue", vtype=bool)
        do21:   NC =  NC(suffix="ctrl.arrDO[20].bValue", vtype=bool)
        do22:   NC =  NC(suffix="ctrl.arrDO[21].bValue", vtype=bool)
        do23:   NC =  NC(suffix="ctrl.arrDO[22].bValue", vtype=bool)
        do24:   NC =  NC(suffix="ctrl.arrDO[23].bValue", vtype=bool)
        do25:   NC =  NC(suffix="ctrl.arrDO[24].bValue", vtype=bool)
        do26:   NC =  NC(suffix="ctrl.arrDO[25].bValue", vtype=bool)
        do27:   NC =  NC(suffix="ctrl.arrDO[26].bValue", vtype=bool)
        do28:   NC =  NC(suffix="ctrl.arrDO[27].bValue", vtype=bool)
        do29:   NC =  NC(suffix="ctrl.arrDO[28].bValue", vtype=bool)
        do30:   NC =  NC(suffix="ctrl.arrDO[29].bValue", vtype=bool)
        do31:   NC =  NC(suffix="ctrl.arrDO[30].bValue", vtype=bool)
        do32:   NC =  NC(suffix="ctrl.arrDO[31].bValue", vtype=bool)








