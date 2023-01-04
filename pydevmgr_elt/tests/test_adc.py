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


def test_adc_data_matching():
    
    adc = Adc()
    from pydevmgr_elt_qt.elt_device_ctrl import EltDeviceCtrl
    from pydevmgr_elt import open_device

    class MotorCtrStatData(EltDeviceCtrl.Data.StatData):
        pos_actual: NodeVar[float] = 0.0
        pos_error:  NodeVar[float] = 0.0
        pos_target: NodeVar[float] = 0.0
        vel_actual: NodeVar[float] = 0.0

    class MotorCtrData(EltDeviceCtrl.Data):
        StatData =  MotorCtrStatData               
        stat: StatData = StatData()  
   
    class AdcData(BaseModel):
        
        motor1= MotorCtrData()
        motor2= MotorCtrData()
        
    data = AdcData()

    dl = DataLink(adc, data)
    data.motor1.stat.pos_actual 

test_adc_data_matching()
