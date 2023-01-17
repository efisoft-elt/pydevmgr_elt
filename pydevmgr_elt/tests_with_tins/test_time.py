from pydevmgr_core.base.base import find_factories
from pydevmgr_core.base.dataclass import create_data_model
from pydevmgr_core.base.datamodel import DataLink
from pydevmgr_core.base.node import BaseNode
from pydevmgr_ua.uanode import UaNode
from pydevmgr_elt import Time
import os


LIVE = True 
LIVE = os.environ.get("ELT_TEST", False)

def test_time_stat():
    time = Time( prefix="MAIN.timer", address="opc.tcp://192.168.1.11:4840")
    Data = time.Stat.Data
    #Data = create_data_model( "Data", find_factories(Time.Stat, BaseNode))
    data = Data()
    with time:
        DataLink( time.stat, data).download()
    print( data ) 


def test_time_cfg():
    time = Time( prefix="MAIN.timer", address="opc.tcp://192.168.1.11:4840")
    Data = time.Cfg.Data
    # Data = create_data_model( "Data", find_factories(Time.Stat, BaseNode))
    data = Data()
    with time:
        DataLink( time.cfg, data).download()
    print( data ) 
test_time_cfg()
