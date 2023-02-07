from pydevmgr_elt import Motor 

def test_some_data():

    assert Motor.Data().stat.pos_actual == 0.0
    assert Motor.Data().cfg.backlash == 0.0
