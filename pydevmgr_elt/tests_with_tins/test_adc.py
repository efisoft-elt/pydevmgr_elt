from enum import Enum
from pydevmgr_core.base.base import find_factories
from pydevmgr_core.base import create_data_model, DataLink
from pydevmgr_core.base.node import BaseNode
from pydevmgr_ua.uanode import UaNode
from pydevmgr_elt import Adc 
import os 

LIVE = os.environ.get("ELT_TEST", False)



def test_adc_cfg_live():
    if not LIVE: return 

    adc = Adc( prefix="MAIN.adc1", address="opc.tcp://192.168.1.11:4840")
    data = adc.Cfg.Data()
    with adc:
        DataLink( adc.cfg, data).download()
    print( data)

def test_adc_stat_live():
    if not LIVE: return 

    adc = Adc( prefix="MAIN.adc1", address="opc.tcp://192.168.1.11:4840")
    Data = create_data_model( "Data", find_factories(  adc.Stat, BaseNode))

    data = Data()
    with adc:
        DataLink( adc.stat, data).download()
    print(data)
    data.error_code = 7123657123
    


test_adc_cfg_live()
test_adc_stat_live()
