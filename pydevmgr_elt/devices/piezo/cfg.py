from pydevmgr_core import  NodeVar
from pydevmgr_core.base.dataclass import set_data_model
from pydevmgr_elt.base import EltDevice,  GROUP
from pydevmgr_elt.base.tools import _inc, enum_group, enum_txt

from enum import Enum
Base = EltDevice.Cfg

N = Base.Node # Base Node
NC = N.Config
NV = NodeVar # used in Data 


@set_data_model
class PiezoCfg(Base):
    class Config(Base.Config):
        full_range1:          NC  =  NC(suffix='cfg.nFullRange[0].nValue',          vtype=int,  parser='UaInt16')
        full_range2:          NC  =  NC(suffix='cfg.nFullRange[1].nValue',          vtype=int,  parser='UaInt16')
        full_range3:          NC  =  NC(suffix='cfg.nFullRange[2].nValue',          vtype=int,  parser='UaInt16')
        home1:                NC  =  NC(suffix='cfg.nHome[0].nValue',               vtype=int,  parser='UaInt16')
        home2:                NC  =  NC(suffix='cfg.nHome[1].nValue',               vtype=int,  parser='UaInt16')
        home3:                NC  =  NC(suffix='cfg.nHome[2].nValue',               vtype=int,  parser='UaInt16')
        lower_limit1:         NC  =  NC(suffix='cfg.nLimitLow[0].nValue',           vtype=int,  parser='UaInt16')
        lower_limit2:         NC  =  NC(suffix='cfg.nLimitLow[1].nValue',           vtype=int,  parser='UaInt16')
        lower_limit3:         NC  =  NC(suffix='cfg.nLimitLow[2].nValue',           vtype=int,  parser='UaInt16')
        max_on:               NC  =  NC(suffix='cfg.nMaxOn',                        vtype=int,  parser='UaInt32')
        num_axis:             NC  =  NC(suffix='cfg.nNumAxes',                      vtype=int,  parser='UaInt16')
        upper_limit1:         NC  =  NC(suffix='cfg.nLimitHigh[0].nValue',          vtype=int,  parser='UaInt16')
        upper_limit2:         NC  =  NC(suffix='cfg.nLimitHigh[1].nValue',          vtype=int,  parser='UaInt16')
        upper_limit3:         NC  =  NC(suffix='cfg.nLimitHigh[2].nValue',          vtype=int,  parser='UaInt16')
        user_offset_input1:   NC  =  NC(suffix='cfg.nUserOffsetBit_Get[0].nValue',  vtype=int,  parser='UaInt16')
        user_offset_input2:   NC  =  NC(suffix='cfg.nUserOffsetBit_Get[1].nValue',  vtype=int,  parser='UaInt16')
        user_offset_input3:   NC  =  NC(suffix='cfg.nUserOffsetBit_Get[2].nValue',  vtype=int,  parser='UaInt16')
        user_offset_output1:  NC  =  NC(suffix='cfg.nUserOffsetBit_Set[0].nValue',  vtype=int,  parser='UaInt16')
        user_offset_output2:  NC  =  NC(suffix='cfg.nUserOffsetBit_Set[1].nValue',  vtype=int,  parser='UaInt16')
        user_offset_output3:  NC  =  NC(suffix='cfg.nUserOffsetBit_Set[2].nValue',  vtype=int,  parser='UaInt16')
        user_to_bit_input1:   NC  =  NC(suffix='cfg.lrUser2Bit_Get[0].lrValue'      ,           vtype=int)
        user_to_bit_input2:   NC  =  NC(suffix='cfg.lrUser2Bit_Get[1].lrValue'      ,           vtype=int)
        user_to_bit_input3:   NC  =  NC(suffix='cfg.lrUser2Bit_Get[2].lrValue'      ,           vtype=int)
        user_to_bit_output1:  NC  =  NC(suffix='cfg.lrUser2Bit_Set[0].lrValue'      ,           vtype=int)
        user_to_bit_output2:  NC  =  NC(suffix='cfg.lrUser2Bit_Set[1].lrValue'      ,           vtype=int)
        user_to_bit_output3:  NC  =  NC(suffix='cfg.lrUser2Bit_Set[2].lrValue'      ,           vtype=int)


if __name__ == "__main__":
    PiezoCfg()
