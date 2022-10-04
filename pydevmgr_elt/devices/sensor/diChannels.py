from pydevmgr_core import  NodeAlias1, Defaults, NodeVar
from pydevmgr_elt.base import EltDevice,  GROUP
from pydevmgr_elt.base.tools import _inc, enum_group, enum_txt

from enum import Enum

Base = EltDevice.Interface

N = Base.Node # Base Node
NC = N.Config
ND = Defaults[NC] # this typing var says that it is a Node object holding default values 
NV = NodeVar # used in Data 

    


class DiChannels(Base):
    class Config(Base.Config):
        di1:              ND =  NC(suffix="stat.arrDI[0].bValue")
        di2:              ND =  NC(suffix="stat.arrDI[1].bValue")
        di3:              ND =  NC(suffix="stat.arrDI[2].bValue")
        di4:              ND =  NC(suffix="stat.arrDI[3].bValue")  
        di5:               ND =  NC(suffix="stat.arrDI[4].bValue")
        di6:               ND =  NC(suffix="stat.arrDI[5].bValue")
        di7:               ND =  NC(suffix="stat.arrDI[6].bValue")
        di8:               ND =  NC(suffix="stat.arrDI[7].bValue")
        di9:               ND =  NC(suffix="stat.arrDI[8].bValue")
        di10:              ND =  NC(suffix="stat.arrDI[9].bValue")
        di11:              ND =  NC(suffix="stat.arrDI[10].bValue")
        di12:              ND =  NC(suffix="stat.arrDI[11].bValue")
        di13:              ND =  NC(suffix="stat.arrDI[12].bValue")
        di14:              ND =  NC(suffix="stat.arrDI[13].bValue")
        di15:              ND =  NC(suffix="stat.arrDI[14].bValue")
        di16:              ND =  NC(suffix="stat.arrDI[15].bValue")

        di17:              ND =  NC(suffix="stat.arrDI[16].bValue")
        di18:              ND =  NC(suffix="stat.arrDI[17].bValue")
        di19:              ND =  NC(suffix="stat.arrDI[18].bValue")
        di20:              ND =  NC(suffix="stat.arrDI[19].bValue")
        di21:              ND =  NC(suffix="stat.arrDI[20].bValue")
        di22:              ND =  NC(suffix="stat.arrDI[21].bValue")
        di23:              ND =  NC(suffix="stat.arrDI[22].bValue")
        di24:              ND =  NC(suffix="stat.arrDI[23].bValue")
        di25:              ND =  NC(suffix="stat.arrDI[24].bValue")
        di26:              ND =  NC(suffix="stat.arrDI[25].bValue")
        di27:              ND =  NC(suffix="stat.arrDI[26].bValue")
        di28:              ND =  NC(suffix="stat.arrDI[27].bValue")
        di29:              ND =  NC(suffix="stat.arrDI[28].bValue")
        di30:              ND =  NC(suffix="stat.arrDI[29].bValue")
        di31:              ND =  NC(suffix="stat.arrDI[30].bValue")
        di32:              ND =  NC(suffix="stat.arrDI[31].bValue")



