

from pydevmgr_core import  NodeAlias1, Defaults, NodeVar
from pydevmgr_elt.base import EltDevice  

from enum import Enum

Base = EltDevice.Interface

N = Base.Node # Base Node
NC = N.Config
ND = Defaults[NC] # this typing var says that it is a Node object holding default values 
NV = NodeVar # used in Data 



class AoChannels(Base):
    class Config(Base.Config):
        ao1:               ND =  NC(suffix="ctrl.arrAO[0].lrValueUser")
        ao2:               ND =  NC(suffix="ctrl.arrAO[1].lrValueUser")
        ao3:               ND =  NC(suffix="ctrl.arrAO[2].lrValueUser")
        ao4:               ND =  NC(suffix="ctrl.arrAO[3].lrValueUser")  
        ao5:               ND =  NC(suffix="ctrl.arrAO[4].lrValueUser")
        ao6:               ND =  NC(suffix="ctrl.arrAO[5].lrValueUser")
        ao7:               ND =  NC(suffix="ctrl.arrAO[6].lrValueUser")
        ao8:               ND =  NC(suffix="ctrl.arrAO[7].lrValueUser")
        ao9:               ND =  NC(suffix="ctrl.arrAO[8].lrValueUser")
        ao10:              ND =  NC(suffix="ctrl.arrAO[9].lrValueUser")
        ao11:              ND =  NC(suffix="ctrl.arrAO[10].lrValueUser")
        ao12:              ND =  NC(suffix="ctrl.arrAO[11].lrValueUser")
        ao13:              ND =  NC(suffix="ctrl.arrAO[12].lrValueUser")
        ao14:              ND =  NC(suffix="ctrl.arrAO[13].lrValueUser")
        ao15:              ND =  NC(suffix="ctrl.arrAO[14].lrValueUser")
        ao16:              ND =  NC(suffix="ctrl.arrAO[15].lrValueUser")

        ao17:              ND =  NC(suffix="ctrl.arrAO[16].lrValueUser")
        ao18:              ND =  NC(suffix="ctrl.arrAO[17].lrValueUser")
        ao19:              ND =  NC(suffix="ctrl.arrAO[18].lrValueUser")
        ao20:              ND =  NC(suffix="ctrl.arrAO[19].lrValueUser")
        ao21:              ND =  NC(suffix="ctrl.arrAO[20].lrValueUser")
        ao22:              ND =  NC(suffix="ctrl.arrAO[21].lrValueUser")
        ao23:              ND =  NC(suffix="ctrl.arrAO[22].lrValueUser")
        ao24:              ND =  NC(suffix="ctrl.arrAO[23].lrValueUser")
        ao25:              ND =  NC(suffix="ctrl.arrAO[24].lrValueUser")
        ao26:              ND =  NC(suffix="ctrl.arrAO[25].lrValueUser")
        ao27:              ND =  NC(suffix="ctrl.arrAO[26].lrValueUser")
        ao28:              ND =  NC(suffix="ctrl.arrAO[27].lrValueUser")
        ao29:              ND =  NC(suffix="ctrl.arrAO[28].lrValueUser")
        ao30:              ND =  NC(suffix="ctrl.arrAO[29].lrValueUser")
        ao31:              ND =  NC(suffix="ctrl.arrAO[30].lrValueUser")
        ao32:              ND =  NC(suffix="ctrl.arrAO[31].lrValueUser")

