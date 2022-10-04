
from pydevmgr_core import  NodeAlias1, Defaults, NodeVar
from pydevmgr_elt.base import EltDevice

from enum import Enum

Base = EltDevice.Interface

N = Base.Node # Base Node
NC = N.Config
ND = Defaults[NC] # this typing var says that it is a Node object holding default values 
NV = NodeVar # used in Data 




    
class AiChannels(Base):
    class Config(Base.Config):
        ai1:               ND =  NC(suffix="stat.arrAI[0].lrValueUser")
        ai2:               ND =  NC(suffix="stat.arrAI[1].lrValueUser")
        ai3:               ND =  NC(suffix="stat.arrAI[2].lrValueUser")
        ai4:               ND =  NC(suffix="stat.arrAI[3].lrValueUser")  
        ai5:               ND =  NC(suffix="stat.arrAI[4].lrValueUser")
        ai6:               ND =  NC(suffix="stat.arrAI[5].lrValueUser")
        ai7:               ND =  NC(suffix="stat.arrAI[6].lrValueUser")
        ai8:               ND =  NC(suffix="stat.arrAI[7].lrValueUser")
        ai9:               ND =  NC(suffix="stat.arrAI[8].lrValueUser")
        ai10:              ND =  NC(suffix="stat.arrAI[9].lrValueUser")
        ai11:              ND =  NC(suffix="stat.arrAI[10].lrValueUser")
        ai12:              ND =  NC(suffix="stat.arrAI[11].lrValueUser")
        ai13:              ND =  NC(suffix="stat.arrAI[12].lrValueUser")
        ai14:              ND =  NC(suffix="stat.arrAI[13].lrValueUser")
        ai15:              ND =  NC(suffix="stat.arrAI[14].lrValueUser")
        ai16:              ND =  NC(suffix="stat.arrAI[15].lrValueUser")

        ai17:               ND =  NC(suffix="stat.arrAI[16].lrValueUser")
        ai18:               ND =  NC(suffix="stat.arrAI[17].lrValueUser")
        ai19:               ND =  NC(suffix="stat.arrAI[18].lrValueUser")
        ai20:               ND =  NC(suffix="stat.arrAI[19].lrValueUser")
        ai21:               ND =  NC(suffix="stat.arrAI[20].lrValueUser")
        ai22:               ND =  NC(suffix="stat.arrAI[21].lrValueUser")
        ai23:               ND =  NC(suffix="stat.arrAI[22].lrValueUser")
        ai24:               ND =  NC(suffix="stat.arrAI[23].lrValueUser")
        ai25:               ND =  NC(suffix="stat.arrAI[24].lrValueUser")
        ai26:               ND =  NC(suffix="stat.arrAI[25].lrValueUser")
        ai27:               ND =  NC(suffix="stat.arrAI[26].lrValueUser")
        ai28:               ND =  NC(suffix="stat.arrAI[27].lrValueUser")
        ai29:               ND =  NC(suffix="stat.arrAI[28].lrValueUser")
        ai30:               ND =  NC(suffix="stat.arrAI[29].lrValueUser")
        ai31:               ND =  NC(suffix="stat.arrAI[30].lrValueUser")
        ai32:               ND =  NC(suffix="stat.arrAI[31].lrValueUser")



    








