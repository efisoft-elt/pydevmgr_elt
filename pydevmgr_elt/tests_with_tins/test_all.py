import time
from pydevmgr_core.base.base import BaseObject, find_factories
from pydevmgr_core.base.dataclass import ClassesToDataModelExtractor, create_data_model, set_data_model
from pydevmgr_core.base.datamodel import DataLink
from pydevmgr_ua import UaDevice
from pydevmgr_elt.devices.adc import Adc
from pydevmgr_elt.devices.ccssim import CcsSim
from pydevmgr_elt.devices.drot import Drot
from pydevmgr_elt.devices.lamp import Lamp

from pydevmgr_elt.devices.motor import Motor
from pydevmgr_elt.devices.shutter import Shutter
from pydevmgr_elt.devices.time import Time 



@set_data_model
class Main(UaDevice):
    class Config:
        motor1 = Motor.Config( prefix="Motor1")
        motor2 = Motor.Config( prefix="Motor2")
        drot = Drot.Config( prefix="drot1")
        adc = Adc.Config( prefix="adc1") 
        shutter = Shutter.Config( prefix="Shutter1")
        lamp = Lamp.Config( prefix="Lamp1")
        timer = Time.Config( prefix="timer")
        ccs = CcsSim.Config( prefix="ccs_sim")


if __name__ == "__main__":
    m = Main( prefix="MAIN", address="opc.tcp://192.168.1.11:4840")
    Data = create_data_model("Data",find_factories(Main, BaseObject), depth=100)  
    data = Data()
    
    dl = DataLink(m, data)
    
    with m:
        tic = time.time()
        for i in range(1):
            dl.download() 
        toc = time.time()
    print("data",  data) 
    print( (toc-tic) ) 
    assert data.motor1.__class__ is data.motor2.__class__
