
from pydevmgr_core import   NodeVar
from pydevmgr_core.base.dataclass import set_data_model
from pydevmgr_elt.base import EltDevice


Base = EltDevice.Interface

N = Base.Node # Base Node
NC = N.Config
NV = NodeVar # used in Data 

@set_data_model
class AiChannels4(Base):
    class Config:
        ai1:    NC =  NC(suffix="stat.arrAI[0].lrValueUser", vtype=float)
        ai2:    NC =  NC(suffix="stat.arrAI[1].lrValueUser", vtype=float)
        ai3:    NC =  NC(suffix="stat.arrAI[2].lrValueUser", vtype=float)
        ai4:    NC =  NC(suffix="stat.arrAI[3].lrValueUser", vtype=float)  

@set_data_model
class AiChannels8(AiChannels4):
    class Config:
        ai1:    NC =  NC(suffix="stat.arrAI[0].lrValueUser", vtype=float)
        ai2:    NC =  NC(suffix="stat.arrAI[1].lrValueUser", vtype=float)
        ai3:    NC =  NC(suffix="stat.arrAI[2].lrValueUser", vtype=float)
        ai4:    NC =  NC(suffix="stat.arrAI[3].lrValueUser", vtype=float)  
        ai5:    NC =  NC(suffix="stat.arrAI[4].lrValueUser", vtype=float)
        ai6:    NC =  NC(suffix="stat.arrAI[5].lrValueUser", vtype=float)
        ai7:    NC =  NC(suffix="stat.arrAI[6].lrValueUser", vtype=float)
        ai8:    NC =  NC(suffix="stat.arrAI[7].lrValueUser", vtype=float)

@set_data_model
class AiChannels16(AiChannels8):
    class Config:
        ai9:    NC =  NC(suffix="stat.arrAI[8].lrValueUser", vtype=float)
        ai10:   NC =  NC(suffix="stat.arrAI[9].lrValueUser", vtype=float)
        ai11:   NC =  NC(suffix="stat.arrAI[10].lrValueUser", vtype=float)
        ai12:   NC =  NC(suffix="stat.arrAI[11].lrValueUser", vtype=float)
        ai13:   NC =  NC(suffix="stat.arrAI[12].lrValueUser", vtype=float)
        ai14:   NC =  NC(suffix="stat.arrAI[13].lrValueUser", vtype=float)
        ai15:   NC =  NC(suffix="stat.arrAI[14].lrValueUser", vtype=float)
        ai16:   NC =  NC(suffix="stat.arrAI[15].lrValueUser", vtype=float)

@set_data_model
class AiChannels32(AiChannels16):
    class Config:
        ai17:    NC =  NC(suffix="stat.arrAI[16].lrValueUser", vtype=float)
        ai18:    NC =  NC(suffix="stat.arrAI[17].lrValueUser", vtype=float)
        ai19:    NC =  NC(suffix="stat.arrAI[18].lrValueUser", vtype=float)
        ai20:    NC =  NC(suffix="stat.arrAI[19].lrValueUser", vtype=float)
        ai21:    NC =  NC(suffix="stat.arrAI[20].lrValueUser", vtype=float)
        ai22:    NC =  NC(suffix="stat.arrAI[21].lrValueUser", vtype=float)
        ai23:    NC =  NC(suffix="stat.arrAI[22].lrValueUser", vtype=float)
        ai24:    NC =  NC(suffix="stat.arrAI[23].lrValueUser", vtype=float)
        ai25:    NC =  NC(suffix="stat.arrAI[24].lrValueUser", vtype=float)
        ai26:    NC =  NC(suffix="stat.arrAI[25].lrValueUser", vtype=float)
        ai27:    NC =  NC(suffix="stat.arrAI[26].lrValueUser", vtype=float)
        ai28:    NC =  NC(suffix="stat.arrAI[27].lrValueUser", vtype=float)
        ai29:    NC =  NC(suffix="stat.arrAI[28].lrValueUser", vtype=float)
        ai30:    NC =  NC(suffix="stat.arrAI[29].lrValueUser", vtype=float)
        ai31:    NC =  NC(suffix="stat.arrAI[30].lrValueUser", vtype=float)
        ai32:    NC =  NC(suffix="stat.arrAI[31].lrValueUser", vtype=float)


    








