from pydevmgr_core import    NodeVar
from pydevmgr_elt.devices.motor import Motor
Base = Motor.Cfg


N = Base.Node # Base Node
NC = N.Config
NV = NodeVar # used in Data 



class DrotCfg(Base):
    class Config(Base.Config):
        dir_sign: NC = NC(suffix='cfg.nDirSign', parser='UaInt32')
        focus_sign: NC = NC(suffix='cfg.nFocusSign', parser='UaInt32')
        trk_period: NC = NC(suffix='cfg.nMinSkipCycles', parser='UaInt32')

        stat_ref:           NC = NC(suffix="cfg.lrStatRef", parser=float)
        sky_ref:            NC = NC(suffix="cfg.lrSkyRef", parser=float)
        elev_ref:           NC = NC(suffix="cfg.lrElevRef", parser=float)
        user_ref:           NC = NC(suffix="cfg.lrUserRef", parser=float)
        user_par1:          NC = NC(suffix="cfg.lrUserPar1", parser=float)
        user_par2:          NC = NC(suffix="cfg.lrUserPar2", parser=float)
        user_par3:          NC = NC(suffix="cfg.lrUserPar3", parser=float)
        user_par4:          NC = NC(suffix="cfg.lrUserPar4", parser=float)
        latitude:           NC = NC(suffix="cfg.site.latitude", parser=float)
        longitude:          NC = NC(suffix="cfg.site.longitude", parser=float) 
        trk_threshold:      NC = NC(suffix="cfg.lrTrkThreshold", parser=float)

        active_low_index:   NC =  NC(suffix='motor.cfg.bArrActiveLow[3].bValue'  )
        active_low_lhw:     NC =  NC(suffix='motor.cfg.bArrActiveLow[1].bValue'  )
        active_low_lstop:   NC =  NC(suffix='motor.cfg.bArrActiveLow[0].bValue'  )
        active_low_ref:     NC =  NC(suffix='motor.cfg.bArrActiveLow[2].bValue'  )
        active_low_uhw:     NC =  NC(suffix='motor.cfg.bArrActiveLow[4].bValue'  )
        active_low_ustop:   NC =  NC(suffix='motor.cfg.bArrActiveLow[5].bValue'  )
        axis_type:          NC =  NC(suffix='motor.cfg.nAxisType',               parser='AxisType')
        backlash:           NC =  NC(suffix='motor.cfg.lrBacklash'               )
        brake:              NC =  NC(suffix='motor.cfg.bUseBrake'                )
        check_inpos:        NC =  NC(suffix='motor.cfg.bCheckInPos'              )
        disable:            NC =  NC(suffix='motor.cfg.bDisableAfterMove'        )
        exec_post_init:     NC =  NC(suffix='motor.cfg.bExecUserPostInit'        )
        exec_post_move:     NC =  NC(suffix='motor.cfg.bExecUserPostMove'        )
        exec_pre_init:      NC =  NC(suffix='motor.cfg.bExecUserPreInit'         )
        exec_pre_move:      NC =  NC(suffix='motor.cfg.bExecUserPreMove'         )
        init_seq1_action:   NC =  NC(suffix='motor.cfg.strArrInitSeq[1].nAction',   parser='UaInt32')
        init_seq1_value1:   NC =  NC(suffix='motor.cfg.strArrInitSeq[1].lrValue1'   )
        init_seq1_value2:   NC =  NC(suffix='motor.cfg.strArrInitSeq[1].lrValue2'   )
        init_seq2_action:   NC =  NC(suffix='motor.cfg.strArrInitSeq[2].nAction',   parser='UaInt32')
        init_seq2_value1:   NC =  NC(suffix='motor.cfg.strArrInitSeq[2].lrValue1'   )
        init_seq2_value2:   NC =  NC(suffix='motor.cfg.strArrInitSeq[2].lrValue2'   )
        init_seq3_action:   NC =  NC(suffix='motor.cfg.strArrInitSeq[3].nAction',   parser='UaInt32')
        init_seq3_value1:   NC =  NC(suffix='motor.cfg.strArrInitSeq[3].lrValue1'   )
        init_seq3_value2:   NC =  NC(suffix='motor.cfg.strArrInitSeq[3].lrValue2'   )
        init_seq4_action:   NC =  NC(suffix='motor.cfg.strArrInitSeq[4].nAction',   parser='UaInt32')
        init_seq4_value1:   NC =  NC(suffix='motor.cfg.strArrInitSeq[4].lrValue1'   )
        init_seq4_value2:   NC =  NC(suffix='motor.cfg.strArrInitSeq[4].lrValue2'   )
        init_seq5_action:   NC =  NC(suffix='motor.cfg.strArrInitSeq[5].nAction',   parser='UaInt32')
        init_seq5_value1:   NC =  NC(suffix='motor.cfg.strArrInitSeq[5].lrValue1'   )
        init_seq5_value2:   NC =  NC(suffix='motor.cfg.strArrInitSeq[5].lrValue2'   )
        init_seq6_action:   NC =  NC(suffix='motor.cfg.strArrInitSeq[6].nAction',   parser='UaInt32')
        init_seq6_value1:   NC =  NC(suffix='motor.cfg.strArrInitSeq[6].lrValue1'   )
        init_seq6_value2:   NC =  NC(suffix='motor.cfg.strArrInitSeq[6].lrValue2'   )
        init_seq7_action:   NC =  NC(suffix='motor.cfg.strArrInitSeq[7].nAction',   parser='UaInt32')
        init_seq7_value1:   NC =  NC(suffix='motor.cfg.strArrInitSeq[7].lrValue1'   )
        init_seq7_value2:   NC =  NC(suffix='motor.cfg.strArrInitSeq[7].lrValue2'   )
        init_seq8_action:   NC =  NC(suffix='motor.cfg.strArrInitSeq[8].nAction',   parser='UaInt32')
        init_seq8_value1:   NC =  NC(suffix='motor.cfg.strArrInitSeq[8].lrValue1'   )
        init_seq8_value2:   NC =  NC(suffix='motor.cfg.strArrInitSeq[8].lrValue2'   )
        init_seq9_action:   NC =  NC(suffix='motor.cfg.strArrInitSeq[9].nAction',   parser='UaInt32')
        init_seq9_value1:   NC =  NC(suffix='motor.cfg.strArrInitSeq[9].lrValue1'   )
        init_seq9_value2:   NC =  NC(suffix='motor.cfg.strArrInitSeq[9].lrValue2'   )
        init_seq10_action:  NC =  NC(suffix='motor.cfg.strArrInitSeq[10].nAction',  parser='UaInt32')
        init_seq10_value1:  NC =  NC(suffix='motor.cfg.strArrInitSeq[10].lrValue1'  )
        init_seq10_value2:  NC =  NC(suffix='motor.cfg.strArrInitSeq[10].lrValue2'  )
        lock:               NC =  NC(suffix='motor.cfg.bLock'                       )
        lock_pos:           NC =  NC(suffix='motor.cfg.lrLockPos'                   )
        lock_tolerance:     NC =  NC(suffix='motor.cfg.lrLockTol'                   )
        low_brake:          NC =  NC(suffix='motor.cfg.bActiveLowBrake'             )
        low_inpos:          NC =  NC(suffix='motor.cfg.bActiveLowInPos'             )
        max_pos:            NC =  NC(suffix='motor.cfg.lrMaxPosition'               )
        min_pos:            NC =  NC(suffix='motor.cfg.lrMinPosition'               )
        tout_init:          NC =  NC(suffix='motor.cfg.nTimeoutInit',               parser='UaInt32')
        tout_move:          NC =  NC(suffix='motor.cfg.nTimeoutMove',               parser='UaInt32')
        tout_switch:        NC =  NC(suffix='motor.cfg.nTimeoutSwitch',             parser='UaInt32')
        velocity:           NC =  NC(suffix='motor.cfg.lrDefaultVelocity'           )
  


    class Data(Base.Data):
        dir_sign: NV[int] = 0
        focus_sign: NV[int] = 0
        trk_period: NV[int] = 0

