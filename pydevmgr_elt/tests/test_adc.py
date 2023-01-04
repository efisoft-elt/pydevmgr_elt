from pydantic.main import BaseModel
from pydevmgr_core.base.datamodel import DataLink, NodeVar
import pytest 
from pydevmgr_elt import Adc 




def test_adc_default_motor():
    adc = Adc( prefix="MAIN.adc")
    
    assert adc.motor1.engine.prefix == "MAIN.adc.motor1"


def test_adc_configured_motor():

    adc = Adc( prefix="MAIN.adc",   motors=[ {"prefix":"motor9"}, {"prefix":"motor10"}] )
    
    
    assert adc.motor1.engine.prefix == "MAIN.adc.motor9"
    assert adc.motor2.engine.prefix == "MAIN.adc.motor10"


def test_adc_motor_can_be_found():
    adc = Adc()
    assert len(set(adc.find(Adc.Motor, -1))) == 2
   

def test_adc_motor_factory():
    adc = Adc(prefix="MAIN.adc")
    m = Adc.Config.MotorFactory(prefix="motor999").build(adc)
    adc.motors[0] = m 
    
    assert adc.motor1.engine.prefix == "MAIN.adc.motor999"
    m = Adc.Config.Motor(prefix="motor888").build(adc)
    adc.motors[0] = m 

    
    assert adc.motor1.engine.prefix == "MAIN.adc.motor888"



