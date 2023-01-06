import pytest 
from pydevmgr_elt import Motor


def test_load_map_file():
    
    c = Motor.Config.from_cfgfile("tins/motor1.yml")
    c.load_mapping()

