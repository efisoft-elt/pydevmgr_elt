""" Base on pydevmgr_ua, pydevmgr_elt is defining nodes and methods of ELT standard devices 

All the pydevmgr_core and pydevmgr_ua module members are also included in this package


Example:

:: 

    from pydevmgr_elt import Motor, wait, download

    motor = Motor( address="opc.tcp://myplc.local:4840", prefix="MAIN.Motor1")
    try:
        motor.connect()
        wait( motor.move_abs(2.3, 0.5) ) 
        print( *download( motor.stat.pos_actual, motor.stat.pos_error))
    finally:
        motor.disconnect()

"""
from pydevmgr_core import *

from pydevmgr_ua import  (
        UaInt16, 
        UaInt32, 
        UaInt64, 
        UaUInt16, 
        UaUInt32, 
        UaUInt64, 
        UaFloat, 
        UaDouble,                   
        UaCom, 
        UaDevice, 
        UaNode, 
        UaInterface, 
        UaRpc 
    )


from .base import *
from .devices import * 
from .base import io

