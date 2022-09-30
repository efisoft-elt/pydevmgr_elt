import pytest 
from pydevmgr_elt import Sensor

def test_custom_channel():

    class MySensor(Sensor):
        class Config(Sensor.Config):
            
           temp = Sensor.ChannelFactory(name="temp", map="ai3", type="AI") 
           interlock = Sensor.ChannelFactory(name="interlock", map="di3", type="DI") 

            

    my_sensor = MySensor(channels = [ {'map':'di4', 'name':'door'} ])
    
    assert my_sensor.temp.node == my_sensor.aiChannels.ai3
    assert my_sensor.interlock.node == my_sensor.diChannels.di3
    assert my_sensor.channels[0].config.name == "door" 


test_custom_channel()
