from pydevmgr_core import    NodeVar
from pydevmgr_core.base.dataclass import set_data_model
from pydevmgr_elt.base import EltDevice
from pydevmgr_elt.devices.motor.axis_type import  AXIS_TYPE, AxisType # just needed to record axis type parser
from pydevmgr_elt.devices.motor.init_seq import InitSeq, InitSeqNode, InitSeqNumber, init_sequence_loockup
from enum import Enum
from dataclasses import dataclass
Base = EltDevice.Cfg

N = Base.Node # Base Node
NC = N.Config
NV = NodeVar # used in Data 




@set_data_model    
class MotorCfg(Base):
    AXIS_TYPE = AXIS_TYPE
    InitSeqNumber = InitSeqNumber
    InitSeq = InitSeq
    InitSeqNode = InitSeqNode
    init_sequence_loockup = init_sequence_loockup

    class Config(Base.Config):
        active_low_index:   NC  =  NC(suffix='cfg.bArrActiveLow[3].bValue',     vtype=bool         )
        active_low_lhw:     NC  =  NC(suffix='cfg.bArrActiveLow[1].bValue',     vtype=bool         )
        active_low_lstop:   NC  =  NC(suffix='cfg.bArrActiveLow[0].bValue',     vtype=bool         )
        active_low_ref:     NC  =  NC(suffix='cfg.bArrActiveLow[2].bValue',     vtype=bool         )
        active_low_uhw:     NC  =  NC(suffix='cfg.bArrActiveLow[4].bValue',     vtype=bool         )
        active_low_ustop:   NC  =  NC(suffix='cfg.bArrActiveLow[5].bValue',     vtype=bool         )
        axis_type:          NC  =  NC(suffix='cfg.nAxisType',                   vtype=(AXIS_TYPE,  AXIS_TYPE.LINEAR),  parser='AxisType')
        backlash:           NC  =  NC(suffix='cfg.lrBacklash',                  vtype=float        )
        brake:              NC  =  NC(suffix='cfg.bUseBrake',                   vtype=bool         )
        check_inpos:        NC  =  NC(suffix='cfg.bCheckInPos',                 vtype=bool         )
        disable:            NC  =  NC(suffix='cfg.bDisableAfterMove',           vtype=bool         )
        exec_post_init:     NC  =  NC(suffix='cfg.bExecUserPostInit',           vtype=bool         )
        exec_post_move:     NC  =  NC(suffix='cfg.bExecUserPostMove',           vtype=bool         )
        exec_pre_init:      NC  =  NC(suffix='cfg.bExecUserPreInit',            vtype=bool         )
        exec_pre_move:      NC  =  NC(suffix='cfg.bExecUserPreMove',            vtype=bool         )
        init_seq1_action:   NC  =  NC(suffix='cfg.strArrInitSeq[1].nAction',    vtype=int,         parser='UaInt32')
        init_seq1_value1:   NC  =  NC(suffix='cfg.strArrInitSeq[1].lrValue1',   vtype=float        )
        init_seq1_value2:   NC  =  NC(suffix='cfg.strArrInitSeq[1].lrValue2',   vtype=float        )
        init_seq2_action:   NC  =  NC(suffix='cfg.strArrInitSeq[2].nAction',    vtype=int,         parser='UaInt32')
        init_seq2_value1:   NC  =  NC(suffix='cfg.strArrInitSeq[2].lrValue1',   vtype=float        )
        init_seq2_value2:   NC  =  NC(suffix='cfg.strArrInitSeq[2].lrValue2',   vtype=float        )
        init_seq3_action:   NC  =  NC(suffix='cfg.strArrInitSeq[3].nAction',    vtype=int,         parser='UaInt32')
        init_seq3_value1:   NC  =  NC(suffix='cfg.strArrInitSeq[3].lrValue1',   vtype=float        )
        init_seq3_value2:   NC  =  NC(suffix='cfg.strArrInitSeq[3].lrValue2',   vtype=float        )
        init_seq4_action:   NC  =  NC(suffix='cfg.strArrInitSeq[4].nAction',    vtype=int,         parser='UaInt32')
        init_seq4_value1:   NC  =  NC(suffix='cfg.strArrInitSeq[4].lrValue1',   vtype=float        )
        init_seq4_value2:   NC  =  NC(suffix='cfg.strArrInitSeq[4].lrValue2',   vtype=float        )
        init_seq5_action:   NC  =  NC(suffix='cfg.strArrInitSeq[5].nAction',    vtype=int,         parser='UaInt32')
        init_seq5_value1:   NC  =  NC(suffix='cfg.strArrInitSeq[5].lrValue1',   vtype=float        )
        init_seq5_value2:   NC  =  NC(suffix='cfg.strArrInitSeq[5].lrValue2',   vtype=float        )
        init_seq6_action:   NC  =  NC(suffix='cfg.strArrInitSeq[6].nAction',    vtype=int,         parser='UaInt32')
        init_seq6_value1:   NC  =  NC(suffix='cfg.strArrInitSeq[6].lrValue1',   vtype=float        )
        init_seq6_value2:   NC  =  NC(suffix='cfg.strArrInitSeq[6].lrValue2',   vtype=float        )
        init_seq7_action:   NC  =  NC(suffix='cfg.strArrInitSeq[7].nAction',    vtype=int,         parser='UaInt32')
        init_seq7_value1:   NC  =  NC(suffix='cfg.strArrInitSeq[7].lrValue1',   vtype=float        )
        init_seq7_value2:   NC  =  NC(suffix='cfg.strArrInitSeq[7].lrValue2',   vtype=float        )
        init_seq8_action:   NC  =  NC(suffix='cfg.strArrInitSeq[8].nAction',    vtype=int,         parser='UaInt32')
        init_seq8_value1:   NC  =  NC(suffix='cfg.strArrInitSeq[8].lrValue1',   vtype=float        )
        init_seq8_value2:   NC  =  NC(suffix='cfg.strArrInitSeq[8].lrValue2',   vtype=float        )
        init_seq9_action:   NC  =  NC(suffix='cfg.strArrInitSeq[9].nAction',    vtype=int,         parser='UaInt32')
        init_seq9_value1:   NC  =  NC(suffix='cfg.strArrInitSeq[9].lrValue1',   vtype=float        )
        init_seq9_value2:   NC  =  NC(suffix='cfg.strArrInitSeq[9].lrValue2',   vtype=float        )
        init_seq10_action:  NC  =  NC(suffix='cfg.strArrInitSeq[10].nAction',   vtype=int,         parser='UaInt32')
        init_seq10_value1:  NC  =  NC(suffix='cfg.strArrInitSeq[10].lrValue1',  vtype=float        )
        init_seq10_value2:  NC  =  NC(suffix='cfg.strArrInitSeq[10].lrValue2',  vtype=float        )
        lock:               NC  =  NC(suffix='cfg.bLock',                       vtype=bool         )
        lock_pos:           NC  =  NC(suffix='cfg.lrLockPos',                   vtype=float        )
        lock_tolerance:     NC  =  NC(suffix='cfg.lrLockTol',                   vtype=float        )
        low_brake:          NC  =  NC(suffix='cfg.bActiveLowBrake',             vtype=bool         )
        low_inpos:          NC  =  NC(suffix='cfg.bActiveLowInPos',             vtype=bool         )
        max_pos:            NC  =  NC(suffix='cfg.lrMaxPosition',               vtype=float        )
        min_pos:            NC  =  NC(suffix='cfg.lrMinPosition',               vtype=float        )
        tout_init:          NC  =  NC(suffix='cfg.nTimeoutInit',                vtype=int,         parser='UaInt32')
        tout_move:          NC  =  NC(suffix='cfg.nTimeoutMove',                vtype=int,         parser='UaInt32')
        tout_switch:        NC  =  NC(suffix='cfg.nTimeoutSwitch',              vtype=int,         parser='UaInt32')
        velocity:           NC  =  NC(suffix='cfg.lrDefaultVelocity',           vtype=float        )
             
        init_seq1: InitSeqNode.Config = InitSeqNode.Config(seq_number=1)
        init_seq2: InitSeqNode.Config = InitSeqNode.Config(seq_number=2)
        init_seq3: InitSeqNode.Config = InitSeqNode.Config(seq_number=3)
        init_seq4: InitSeqNode.Config = InitSeqNode.Config(seq_number=4)
        init_seq5: InitSeqNode.Config = InitSeqNode.Config(seq_number=5)
        init_seq6: InitSeqNode.Config = InitSeqNode.Config(seq_number=6)
        init_seq7: InitSeqNode.Config = InitSeqNode.Config(seq_number=7)
        init_seq8: InitSeqNode.Config = InitSeqNode.Config(seq_number=8)
        init_seq9: InitSeqNode.Config = InitSeqNode.Config(seq_number=9)
        init_seq10: InitSeqNode.Config = InitSeqNode.Config(seq_number=10)

if __name__=="__main__":
    MotorCfg()

           

