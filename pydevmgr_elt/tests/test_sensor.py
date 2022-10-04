import pytest 
from pydevmgr_elt import Sensor

def test_custom_channel():

    class MySensor(Sensor):
        class Config(Sensor.Config):
            
           temp = Sensor.ChannelAlias.Config(name="temp", map="ai3", type="AI") 
           interlock = Sensor.ChannelAlias.Config(name="interlock", map="di3", type="DI") 

            
    Sensor.ChannelAlias.Config( map='di4', name='door')

    my_sensor = MySensor(channels = [ {'map':'di4', 'name':'door'} ])
    
    assert list(my_sensor.temp.nodes())[0] == my_sensor.aiChannels.ai3
    assert list(my_sensor.interlock.nodes())[0] == my_sensor.diChannels.di3
    assert my_sensor.channels[0].config.name == "door" 


test_custom_channel()

