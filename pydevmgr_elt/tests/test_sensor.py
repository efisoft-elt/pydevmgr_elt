import pytest 
from pydevmgr_elt import Sensor

def test_custom_channel():

    class MySensor(Sensor):
        class Config(Sensor.Config):
            
            temp = Sensor.AiChannel.Config( channel_number = 3)
            interlock = Sensor.DiChannel.Config( channel_number = 3)
            switch = Sensor.DoChannel.Config( channel_number = 3)
            intensity = Sensor.AoChannel.Config( channel_number = 3)

    my_sensor = MySensor()
    
    assert my_sensor.temp.node == my_sensor.aiChannels.ai3
    assert my_sensor.interlock.node == my_sensor.diChannels.di3
    assert my_sensor.switch.node == my_sensor.doChannels.do3
    assert my_sensor.intensity.node  == my_sensor.aoChannels.ao3

