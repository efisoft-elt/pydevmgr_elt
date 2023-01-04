
from pydevmgr_core import   NodeVar
from pydevmgr_elt.base import EltDevice


Base = EltDevice.Interface

N = Base.Node # Base Node
NC = N.Config
NV = NodeVar # used in Data 

class AiChannels4(Base):
    class Config:
        ai1:    NC =  NC(suffix="stat.arrAI[0].lrValueUser")
        ai2:    NC =  NC(suffix="stat.arrAI[1].lrValueUser")
        ai3:    NC =  NC(suffix="stat.arrAI[2].lrValueUser")
        ai4:    NC =  NC(suffix="stat.arrAI[3].lrValueUser")  

class AiChannels8(AiChannels4):
    class Config:
        ai1:    NC =  NC(suffix="stat.arrAI[0].lrValueUser")
        ai2:    NC =  NC(suffix="stat.arrAI[1].lrValueUser")
        ai3:    NC =  NC(suffix="stat.arrAI[2].lrValueUser")
        ai4:    NC =  NC(suffix="stat.arrAI[3].lrValueUser")  
        ai5:    NC =  NC(suffix="stat.arrAI[4].lrValueUser")
        ai6:    NC =  NC(suffix="stat.arrAI[5].lrValueUser")
        ai7:    NC =  NC(suffix="stat.arrAI[6].lrValueUser")
        ai8:    NC =  NC(suffix="stat.arrAI[7].lrValueUser")

class AiChannels16(AiChannels8):
    class Config:
        ai9:    NC =  NC(suffix="stat.arrAI[8].lrValueUser")
        ai10:   NC =  NC(suffix="stat.arrAI[9].lrValueUser")
        ai11:   NC =  NC(suffix="stat.arrAI[10].lrValueUser")
        ai12:   NC =  NC(suffix="stat.arrAI[11].lrValueUser")
        ai13:   NC =  NC(suffix="stat.arrAI[12].lrValueUser")
        ai14:   NC =  NC(suffix="stat.arrAI[13].lrValueUser")
        ai15:   NC =  NC(suffix="stat.arrAI[14].lrValueUser")
        ai16:   NC =  NC(suffix="stat.arrAI[15].lrValueUser")

   
class AiChannels32(AiChannels16):
    class Config:
        ai17:    NC =  NC(suffix="stat.arrAI[16].lrValueUser")
        ai18:    NC =  NC(suffix="stat.arrAI[17].lrValueUser")
        ai19:    NC =  NC(suffix="stat.arrAI[18].lrValueUser")
        ai20:    NC =  NC(suffix="stat.arrAI[19].lrValueUser")
        ai21:    NC =  NC(suffix="stat.arrAI[20].lrValueUser")
        ai22:    NC =  NC(suffix="stat.arrAI[21].lrValueUser")
        ai23:    NC =  NC(suffix="stat.arrAI[22].lrValueUser")
        ai24:    NC =  NC(suffix="stat.arrAI[23].lrValueUser")
        ai25:    NC =  NC(suffix="stat.arrAI[24].lrValueUser")
        ai26:    NC =  NC(suffix="stat.arrAI[25].lrValueUser")
        ai27:    NC =  NC(suffix="stat.arrAI[26].lrValueUser")
        ai28:    NC =  NC(suffix="stat.arrAI[27].lrValueUser")
        ai29:    NC =  NC(suffix="stat.arrAI[28].lrValueUser")
        ai30:    NC =  NC(suffix="stat.arrAI[29].lrValueUser")
        ai31:    NC =  NC(suffix="stat.arrAI[30].lrValueUser")
        ai32:    NC =  NC(suffix="stat.arrAI[31].lrValueUser")


    








