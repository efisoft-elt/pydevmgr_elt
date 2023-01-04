from pydevmgr_core import  NodeVar
from pydevmgr_elt.base import EltDevice


Base = EltDevice.Interface

N = Base.Node # Base Node
NC = N.Config
NV = NodeVar # used in Data 


class DiChannels4(Base):
    class Config:
        di1:   NC =  NC(suffix="stat.arrDI[0].bValue")
        di2:   NC =  NC(suffix="stat.arrDI[1].bValue")
        di3:   NC =  NC(suffix="stat.arrDI[2].bValue")
        di4:   NC =  NC(suffix="stat.arrDI[3].bValue")  



class DiChannels8(DiChannels4):
    class Config:
        di5:    NC =  NC(suffix="stat.arrDI[4].bValue")
        di6:    NC =  NC(suffix="stat.arrDI[5].bValue")
        di7:    NC =  NC(suffix="stat.arrDI[6].bValue")
        di8:    NC =  NC(suffix="stat.arrDI[7].bValue")
   

class DiChannels16(DiChannels8):
    class Config:
        di9:    NC =  NC(suffix="stat.arrDI[8].bValue")
        di10:   NC =  NC(suffix="stat.arrDI[9].bValue")
        di11:   NC =  NC(suffix="stat.arrDI[10].bValue")
        di12:   NC =  NC(suffix="stat.arrDI[11].bValue")
        di13:   NC =  NC(suffix="stat.arrDI[12].bValue")
        di14:   NC =  NC(suffix="stat.arrDI[13].bValue")
        di15:   NC =  NC(suffix="stat.arrDI[14].bValue")
        di16:   NC =  NC(suffix="stat.arrDI[15].bValue")



class DiChannels32(DiChannels16):
    class Config:
        di17:   NC =  NC(suffix="stat.arrDI[16].bValue")
        di18:   NC =  NC(suffix="stat.arrDI[17].bValue")
        di19:   NC =  NC(suffix="stat.arrDI[18].bValue")
        di20:   NC =  NC(suffix="stat.arrDI[19].bValue")
        di21:   NC =  NC(suffix="stat.arrDI[20].bValue")
        di22:   NC =  NC(suffix="stat.arrDI[21].bValue")
        di23:   NC =  NC(suffix="stat.arrDI[22].bValue")
        di24:   NC =  NC(suffix="stat.arrDI[23].bValue")
        di25:   NC =  NC(suffix="stat.arrDI[24].bValue")
        di26:   NC =  NC(suffix="stat.arrDI[25].bValue")
        di27:   NC =  NC(suffix="stat.arrDI[26].bValue")
        di28:   NC =  NC(suffix="stat.arrDI[27].bValue")
        di29:   NC =  NC(suffix="stat.arrDI[28].bValue")
        di30:   NC =  NC(suffix="stat.arrDI[29].bValue")
        di31:   NC =  NC(suffix="stat.arrDI[30].bValue")
        di32:   NC =  NC(suffix="stat.arrDI[31].bValue")



