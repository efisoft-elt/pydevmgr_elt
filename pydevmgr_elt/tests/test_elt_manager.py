import pytest 
from pydevmgr_elt import EltManager, Motor, Lamp
from pydevmgr_elt.base.eltnode import EltNode


def test_create_from_device_dict():

    mgr = EltManager( 'fcf', devices= {'motor1':Motor('motor1'),  'motor2':Motor('motor2') } )
    

    assert mgr.motor1.key == 'motor1'
    
    mgr = EltManager( 'fcf', devices= {'motor1': {'type':'Motor'}, 'motor2':{'type':'Motor'}})
    assert mgr.motor1.key == 'fcf.motor1'
    assert type( mgr.motor1) == Motor

    print( list(mgr.find( Motor, -1)) )
    assert len( list(mgr.find( Motor, -1) )) == 2



def test_create_from_device_list():

    mgr = EltManager( 'fcf', devices=[ Motor('motor1'), Motor('motor2') ] )

    assert mgr.motor1.key == 'motor1'

    mgr = EltManager( 'fcf', devices=[ {'type':'Motor', 'name':'motor1', 'cfgfile':'tins/motor1.yml'} , {'type': 'Motor'} ])
    assert mgr.motor1.key == 'fcf.motor1'


def test_create_devices_from_server_config():

    mgr = EltManager( 'fcf', server={'devices': [ {'type':'Motor', 'name':'motor1', 'cfgfile':'tins/motor1.yml'} ]  } )
     
    assert mgr.motor1.key == 'fcf.motor1'

def test_create_stat_state():
    
    mgr = EltManager( devices={"motor1":Motor.Config(), "lamp":Lamp.Config()})

test_create_stat_state()   
