from pydevmgr_core import  NodeVar
from pydevmgr_core.base.dataclass import set_data_model
from pydevmgr_elt.base import EltDevice


Base = EltDevice.Interface

N = Base.Node # Base Node
NC = N.Config
NV = NodeVar # used in Data 

@set_data_model
class DiChannels4(Base):
    class Config:
        di1:   NC =  NC(suffix="stat.arrDI[0].bValue", vtype=bool)
        di2:   NC =  NC(suffix="stat.arrDI[1].bValue", vtype=bool)
        di3:   NC =  NC(suffix="stat.arrDI[2].bValue", vtype=bool)
        di4:   NC =  NC(suffix="stat.arrDI[3].bValue", vtype=bool)  


@set_data_model
class DiChannels8(DiChannels4):
    class Config:
        di5:    NC =  NC(suffix="stat.arrDI[4].bValue", vtype=bool)
        di6:    NC =  NC(suffix="stat.arrDI[5].bValue", vtype=bool)
        di7:    NC =  NC(suffix="stat.arrDI[6].bValue", vtype=bool)
        di8:    NC =  NC(suffix="stat.arrDI[7].bValue", vtype=bool)
   
@set_data_model
class DiChannels16(DiChannels8):
    class Config:
        di9:    NC =  NC(suffix="stat.arrDI[8].bValue", vtype=bool)
        di10:   NC =  NC(suffix="stat.arrDI[9].bValue", vtype=bool)
        di11:   NC =  NC(suffix="stat.arrDI[10].bValue", vtype=bool)
        di12:   NC =  NC(suffix="stat.arrDI[11].bValue", vtype=bool)
        di13:   NC =  NC(suffix="stat.arrDI[12].bValue", vtype=bool)
        di14:   NC =  NC(suffix="stat.arrDI[13].bValue", vtype=bool)
        di15:   NC =  NC(suffix="stat.arrDI[14].bValue", vtype=bool)
        di16:   NC =  NC(suffix="stat.arrDI[15].bValue", vtype=bool)


@set_data_model
class DiChannels32(DiChannels16):
    class Config:
        di17:   NC =  NC(suffix="stat.arrDI[16].bValue", vtype=bool)
        di18:   NC =  NC(suffix="stat.arrDI[17].bValue", vtype=bool)
        di19:   NC =  NC(suffix="stat.arrDI[18].bValue", vtype=bool)
        di20:   NC =  NC(suffix="stat.arrDI[19].bValue", vtype=bool)
        di21:   NC =  NC(suffix="stat.arrDI[20].bValue", vtype=bool)
        di22:   NC =  NC(suffix="stat.arrDI[21].bValue", vtype=bool)
        di23:   NC =  NC(suffix="stat.arrDI[22].bValue", vtype=bool)
        di24:   NC =  NC(suffix="stat.arrDI[23].bValue", vtype=bool)
        di25:   NC =  NC(suffix="stat.arrDI[24].bValue", vtype=bool)
        di26:   NC =  NC(suffix="stat.arrDI[25].bValue", vtype=bool)
        di27:   NC =  NC(suffix="stat.arrDI[26].bValue", vtype=bool)
        di28:   NC =  NC(suffix="stat.arrDI[27].bValue", vtype=bool)
        di29:   NC =  NC(suffix="stat.arrDI[28].bValue", vtype=bool)
        di30:   NC =  NC(suffix="stat.arrDI[29].bValue", vtype=bool)
        di31:   NC =  NC(suffix="stat.arrDI[30].bValue", vtype=bool)
        di32:   NC =  NC(suffix="stat.arrDI[31].bValue", vtype=bool)



