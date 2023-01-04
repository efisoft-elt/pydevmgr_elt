from os import wait
from pydevmgr_core import  NodeAlias,  NodeVar, BaseNode
from pydevmgr_elt.base import EltDevice
from pydevmgr_elt.devices.motor.axis_type import  AXIS_TYPE, AxisType # just needed to record axis type parser
from pydevmgr_elt.devices.motor.init_seq import InitSeqNumber, init_sequence_loockup
from enum import Enum
from dataclasses import dataclass
Base = EltDevice.Cfg

N = Base.Node # Base Node
NC = N.Config
NV = NodeVar # used in Data 

@dataclass
class InitSeq:
    action_number: InitSeqNumber = InitSeqNumber.END
    value1: float = 0.0
    value2: float = 0.0
    
    @property
    def action_name(self):
        try:
            n = InitSeqNumber(self.action_number)
        except ValueError:
            return ""
        return n.name

class InitSeqNode(NodeAlias):
    """ Alias node returning a structure to handle sequence """
    class Config:
        seq_number: int 
        
    @classmethod
    def new(cls, parent, name, config: Config = None ):
        num = config.seq_number
        nodes =  (f"init_seq{num}_action", 
                  f"init_seq{num}_value1",  
                  f"init_seq{num}_value2")
        config.nodes = nodes
        return super().new(parent, name, config)
    
    def fget(self, action , val1, val2):
        return InitSeq(action, val1, val2)

    def fset(self, init_seq: InitSeq):
        return (init_seq.action_number, init_seq.value1, init_seq.value2)
    
class MotorCfg(Base):
    AXIS_TYPE = AXIS_TYPE
    InitSeqNumber = InitSeqNumber
    init_sequence_loockup = init_sequence_loockup

    class Config(Base.Config):
        active_low_index:   NC =  NC(suffix='cfg.bArrActiveLow[3].bValue'  )
        active_low_lhw:     NC =  NC(suffix='cfg.bArrActiveLow[1].bValue'  )
        active_low_lstop:   NC =  NC(suffix='cfg.bArrActiveLow[0].bValue'  )
        active_low_ref:     NC =  NC(suffix='cfg.bArrActiveLow[2].bValue'  )
        active_low_uhw:     NC =  NC(suffix='cfg.bArrActiveLow[4].bValue'  )
        active_low_ustop:   NC =  NC(suffix='cfg.bArrActiveLow[5].bValue'  )
        axis_type:          NC =  NC(suffix='cfg.nAxisType',               parser='AxisType')
        backlash:           NC =  NC(suffix='cfg.lrBacklash'               )
        brake:              NC =  NC(suffix='cfg.bUseBrake'                )
        check_inpos:        NC =  NC(suffix='cfg.bCheckInPos'              )
        disable:            NC =  NC(suffix='cfg.bDisableAfterMove'        )
        exec_post_init:     NC =  NC(suffix='cfg.bExecUserPostInit'        )
        exec_post_move:     NC =  NC(suffix='cfg.bExecUserPostMove'        )
        exec_pre_init:      NC =  NC(suffix='cfg.bExecUserPreInit'         )
        exec_pre_move:      NC =  NC(suffix='cfg.bExecUserPreMove'         )
        init_seq1_action:   NC =  NC(suffix='cfg.strArrInitSeq[1].nAction',   parser='UaInt32')
        init_seq1_value1:   NC =  NC(suffix='cfg.strArrInitSeq[1].lrValue1'   )
        init_seq1_value2:   NC =  NC(suffix='cfg.strArrInitSeq[1].lrValue2'   )
        init_seq2_action:   NC =  NC(suffix='cfg.strArrInitSeq[2].nAction',   parser='UaInt32')
        init_seq2_value1:   NC =  NC(suffix='cfg.strArrInitSeq[2].lrValue1'   )
        init_seq2_value2:   NC =  NC(suffix='cfg.strArrInitSeq[2].lrValue2'   )
        init_seq3_action:   NC =  NC(suffix='cfg.strArrInitSeq[3].nAction',   parser='UaInt32')
        init_seq3_value1:   NC =  NC(suffix='cfg.strArrInitSeq[3].lrValue1'   )
        init_seq3_value2:   NC =  NC(suffix='cfg.strArrInitSeq[3].lrValue2'   )
        init_seq4_action:   NC =  NC(suffix='cfg.strArrInitSeq[4].nAction',   parser='UaInt32')
        init_seq4_value1:   NC =  NC(suffix='cfg.strArrInitSeq[4].lrValue1'   )
        init_seq4_value2:   NC =  NC(suffix='cfg.strArrInitSeq[4].lrValue2'   )
        init_seq5_action:   NC =  NC(suffix='cfg.strArrInitSeq[5].nAction',   parser='UaInt32')
        init_seq5_value1:   NC =  NC(suffix='cfg.strArrInitSeq[5].lrValue1'   )
        init_seq5_value2:   NC =  NC(suffix='cfg.strArrInitSeq[5].lrValue2'   )
        init_seq6_action:   NC =  NC(suffix='cfg.strArrInitSeq[6].nAction',   parser='UaInt32')
        init_seq6_value1:   NC =  NC(suffix='cfg.strArrInitSeq[6].lrValue1'   )
        init_seq6_value2:   NC =  NC(suffix='cfg.strArrInitSeq[6].lrValue2'   )
        init_seq7_action:   NC =  NC(suffix='cfg.strArrInitSeq[7].nAction',   parser='UaInt32')
        init_seq7_value1:   NC =  NC(suffix='cfg.strArrInitSeq[7].lrValue1'   )
        init_seq7_value2:   NC =  NC(suffix='cfg.strArrInitSeq[7].lrValue2'   )
        init_seq8_action:   NC =  NC(suffix='cfg.strArrInitSeq[8].nAction',   parser='UaInt32')
        init_seq8_value1:   NC =  NC(suffix='cfg.strArrInitSeq[8].lrValue1'   )
        init_seq8_value2:   NC =  NC(suffix='cfg.strArrInitSeq[8].lrValue2'   )
        init_seq9_action:   NC =  NC(suffix='cfg.strArrInitSeq[9].nAction',   parser='UaInt32')
        init_seq9_value1:   NC =  NC(suffix='cfg.strArrInitSeq[9].lrValue1'   )
        init_seq9_value2:   NC =  NC(suffix='cfg.strArrInitSeq[9].lrValue2'   )
        init_seq10_action:  NC =  NC(suffix='cfg.strArrInitSeq[10].nAction',  parser='UaInt32')
        init_seq10_value1:  NC =  NC(suffix='cfg.strArrInitSeq[10].lrValue1'  )
        init_seq10_value2:  NC =  NC(suffix='cfg.strArrInitSeq[10].lrValue2'  )
        lock:               NC =  NC(suffix='cfg.bLock'                       )
        lock_pos:           NC =  NC(suffix='cfg.lrLockPos'                   )
        lock_tolerance:     NC =  NC(suffix='cfg.lrLockTol'                   )
        low_brake:          NC =  NC(suffix='cfg.bActiveLowBrake'             )
        low_inpos:          NC =  NC(suffix='cfg.bActiveLowInPos'             )
        max_pos:            NC =  NC(suffix='cfg.lrMaxPosition'               )
        min_pos:            NC =  NC(suffix='cfg.lrMinPosition'               )
        tout_init:          NC  =  NC(suffix='cfg.nTimeoutInit',               parser='UaInt32')
        tout_move:          NC =  NC(suffix='cfg.nTimeoutMove',               parser='UaInt32')
        tout_switch:        NC =  NC(suffix='cfg.nTimeoutSwitch',             parser='UaInt32')
        velocity:           NC =  NC(suffix='cfg.lrDefaultVelocity'           )
     
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

    class Data(Base.Data):
        active_low_index:   NV[bool]   =  False
        active_low_lhw:     NV[bool]   =  False
        active_low_lstop:   NV[bool]   =  False
        active_low_ref:     NV[bool]   =  False
        active_low_uhw:     NV[bool]   =  False
        active_low_ustop:   NV[bool]   =  False
        axis_type:          NV[int]    =  AXIS_TYPE.LINEAR
        backlash:           NV[float]  =  0.0
        brake:              NV[bool]   =  False
        check_inpos:        NV[bool]   =  False
        disable:            NV[bool]   =  False
        exec_post_init:     NV[bool]   =  False
        exec_post_move:     NV[bool]   =  False
        exec_pre_init:      NV[bool]   =  False
        exec_pre_move:      NV[bool]   =  False
        init_seq10_action:  NV[int]    =  0
        init_seq10_value1:  NV[float]  =  0.0
        init_seq10_value2:  NV[float]  =  0.0
        init_seq1_action:   NV[int]    =  0
        init_seq1_value1:   NV[float]  =  0.0
        init_seq1_value2:   NV[float]  =  0.0
        init_seq2_action:   NV[int]    =  0
        init_seq2_value1:   NV[float]  =  0.0
        init_seq2_value2:   NV[float]  =  0.0
        init_seq3_action:   NV[int]    =  0
        init_seq3_value1:   NV[float]  =  0.0
        init_seq3_value2:   NV[float]  =  0.0
        init_seq4_action:   NV[int]    =  0
        init_seq4_value1:   NV[float]  =  0.0
        init_seq4_value2:   NV[float]  =  0.0
        init_seq5_action:   NV[int]    =  0
        init_seq5_value1:   NV[float]  =  0.0
        init_seq5_value2:   NV[float]  =  0.0
        init_seq6_action:   NV[int]    =  0
        init_seq6_value1:   NV[float]  =  0.0
        init_seq6_value2:   NV[float]  =  0.0
        init_seq7_action:   NV[int]    =  0
        init_seq7_value1:   NV[float]  =  0.0
        init_seq7_value2:   NV[float]  =  0.0
        init_seq8_action:   NV[int]    =  0
        init_seq8_value1:   NV[float]  =  0.0
        init_seq8_value2:   NV[float]  =  0.0
        init_seq9_action:   NV[int]    =  0
        init_seq9_value1:   NV[float]  =  0.0
        init_seq9_value2:   NV[float]  =  0.0
        lock:               NV[bool]   =  False
        lock_pos:           NV[float]  =  0.0
        lock_tolerance:     NV[float]  =  0.0
        low_brake:          NV[bool]   =  False
        low_inpos:          NV[bool]   =  False
        max_pos:            NV[float]  =  0.0
        min_pos:            NV[float]  =  0.0
        tout_init:          NV[int]    =  0
        tout_move:          NV[int]    =  0
        tout_switch:        NV[int]    =  0
        velocity:           NV[float]  =  0.0

        init_seq1: NV[InitSeq] = InitSeq()
        init_seq2: NV[InitSeq] = InitSeq()
        init_seq3: NV[InitSeq] = InitSeq()
        init_seq4: NV[InitSeq] = InitSeq()
        init_seq5: NV[InitSeq] = InitSeq()
        init_seq6: NV[InitSeq] = InitSeq()
        init_seq7: NV[InitSeq] = InitSeq()
        init_seq8: NV[InitSeq] = InitSeq()
        init_seq9: NV[InitSeq] = InitSeq()
        init_seq10: NV[InitSeq] = InitSeq()

if __name__=="__main__":
    MotorCfg()

           

