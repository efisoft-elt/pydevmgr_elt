A Sequence and measurement Script
=================================

The goal here is to build a script to move a motor in several positions and check its true position with a position
sensor. 

The position sensor is a Tesa plugged into the local computer with a serial communication 

To complicate just a bit we will read some values directly on the PLC (not related to any ELT device). They are two
temperature sensors and they are just LREAL values inside the OPC-UA server (PLC).


Tesa device 
-----------

Build a pydevmgr compatible device to communicate withe the Tesa by serial com, you can skip it if not interested. 

.. code-block:: python
    
    from pydevmgr_serial import BaseSerialNode, SerialDevice
    import time 
    from math import nan
     
    class TesaNode(BaseSerialNode, delay= (float,0.01), default=(float, nan)):

        MSG_SIZE = 20
        def fget(self):
            self.com.write(b'?\r')
            self.com.flush()
            time.sleep(self.config.delay)

            sval = self.com.read(self.MSG_SIZE)
            if not sval:
                return self.config.default    
            return float(sval)

    class Tesa(SerialDevice): 
        class Config(SerialDevice.Config): 
            position = TesaNode.Config()

one can use it this way: 

.. code-block:: python 

   tesa = Tesa(port='COM1', baudrate=9600)
   tesa.connect()
   tesa.position.get()
    

OPC-UA Values 
-------------
Outside of the scope of the Elt Low level software we want to read two values

We want also to calibrate them so we can make a ``NodeAlias`` to convert value on the fly. 

.. code-block:: python 

   from pydevmgr_ua import UaNode, UaDevice
   from pydevmgr_core import NodeAlias1, Defaults
   
   # make an alias node to correct a value with a linear law 
   class TempCorector(NodeAlias1, offset=(float, 0.0), slope=(float,1.0) ):
        def fget(self, value):
           return value  * self.config.slope + self.config.offset 

   class Sensors(UaDevice):
        class Config(UaDevice.Config):
            raw_temp1: UaNode.Config = UaNode.Config( suffix="lrTemp1" )
            raw_temp2: UaNode.Config = UaNode.Config( suffix="lrTemp2" )
            
            temp1: Defaults[TempCorector.Config] = TempCorector.Config( node = 'raw_temp1' ) 
            temp2: Defaults[TempCorector.Config] = TempCorector.Config( node = 'raw_temp2' )

It can be used in standalone like this: 

.. code-block:: python

   sensors = Sensors('s', address="opc.tcp://my-plc:4840", prefix="MAIN")
   sensors.temp1.get()


.. note:: 

   The `Defaults` type above insure that the TempCorrector.Config  instantied in the Sensor Config is understood as
   default values, so user do not have the needs to write the 'node' argument in each conf file.


   

A class for the Sequence
------------------------

A pydevmgr BaseManager can be use for generic purpose it can hold several devices or nodes and can use some other
configurations. 

We want to make the position movement configurable, the number of cycles and maybe the data recorded 

.. code-block:: python

   from pydevmgr_core import BaseManager, DequeNode, LocalUtcNode, wait, NodeVar
   from pydevmgr_elt import Motor
   from pydantic import Field
   from typing import List 
   
   class MotorSequence(BaseManager):
        class Config( BaseManager.Config ):
            positions: List[float] = [0.0, 1.0]  # gives some default positions
            n_cycle: int = 1
            velocity: float = 3.0 
            
            time: LocalUtcNode.Config = LocalUtcNode.Config()
            tesa: Tesa.Config = Tesa.Config()
            motor: Motor.Config = Motor.Config()
            sensors: Sensors.Config = Sensors.Config()
            
            seq_data: DequeNode.Config = DequeNode.Config( nodes=['time', 'motor.stat.pos_actual', 'motor.stat.pos_error', 'tesa.position', 'sensors.temp1', 'sensors.temp2'] ) 

        class Data(BaseManager.Data): 
            seq_data: NodeVar[list] = []
            last_pos_encoder: NodeVar[float] = Field(0.0, node="motor.stat.pos_actual")
            last_pos : NodeVar[float] = Field(0.0, node="tesa.position")
            temp1: NodeVar[float] = Field(0.0, node="sensors.temp1")
            temp2: NodeVar[float] = Field(0.0, node="sensors.temp2")
        
        def connect(self): 
            self.motor.connect()
            self.tesa.connect()
            
        def disconnect(self): 
            self.motor.disconnect()
            self.tesa.disconnect()
        
        def init(self):
            self.motor.configure()
            wait( self.motor.reset() )
            wait( self.motor.ini() )
            wait( self.motor.enable() )
            self.seq_data.reset() # empty the dequeue 

        def run(self, callback= lambda : None):
            for pos in self.config.positions * self.config.n_cycle:
                wait( self.motor.move_abs(pos, self.config.velocity) )
                callback() 

        def save_data(self, data, file): 
           
            with open(file,'w') as g:
                # write data header
                g.write(  "\n".join( self.config.seq_data.nodes  ) )
                # write data
                for l in data.seq_data:
                    g.write( ", ".join(str(x) for x in l) )
 

Usage
-----

Let us use this class. But first we can write a configuration file for this to work, and here comes the magic of
pydevmgr. We can make a yaml configuration file as follow  

.. code-block:: yaml 

   motor:
        address: opc.tcp://127.0.0.1:4840 
        prefix: MAIN.Motor1

        ctrl_config:
            backlash: 0.02
            
        # etc .... (see Motor config file )
    sensors:
        temp1:
            offset: 3.4 
            slope: 1.03
        temp2: 
            offset: 3.1
            slope: 1.12
        
    tesa:
        port: COM2
        baudrate: 9600
        bytesize: 8 
        # etc   see pydevmgr_serial
    
    positions: [0.0, -3.0, 0.0, 3.0]
    n_cycle:  10 
    velocity: 0.9

.. code-block:: python

    from pydevmgr_core import DataLink 
    
    seq = MotorSequence.form_cfgfile( 'my-cfg.yml' , key="")
    data = MotorSequence.Data()
    dl = DataLink( seq, data )

    try:
        seq.connect()
        seq.init()
        seq.run( dl.download )
        
    finally:
        seq.save_data(data)
        seq.disconnect()
    



On one file 
-----------

Just the copy / past of everything above


.. code-block:: python 

    from pydevmgr_serial import BaseSerialNode, SerialDevice
    from pydevmgr_ua import UaNode, UaDevice
    from pydevmgr_core import NodeAlias1, Defaults, DataLink
    from pydevmgr_core import BaseManager, DequeNode, LocalUtcNode, wait, NodeVar
    from pydantic import Field
    from pydevmgr_elt import Motor
    from typing import List 
    import time 
    from math import nan
     
    import yaml 

    cfg = yaml.load("""
    motor:
        address: opc.tcp://127.0.0.1:4840 
        prefix: MAIN.Motor1

        ctrl_config:
            backlash: 0.02
            
        # etc .... (see Motor config file )
    sensors:
        temp1:
            offset: 3.4 
            slope: 1.03
        temp2: 
            offset: 3.1
            slope: 1.12
        
    tesa:
        port: COM2
        baudrate: 9600
        bytesize: 8 
        # etc   see pydevmgr_serial
    
    positions: [0.0, -3.0, 0.0, 3.0]
    n_cycle:  10 
    velocity: 0.9
     
    """, Loader=yaml.CLoader)
    



    class TesaNode(BaseSerialNode, delay= (float,0.01), default=(float, nan)):

        MSG_SIZE = 20
        def fget(self):
            self.com.write(b'?\r')
            self.com.flush()
            time.sleep(self.config.delay)

            sval = self.com.read(self.MSG_SIZE)
            if not sval:
                return self.config.default    
            return float(sval)

    class Tesa(SerialDevice): 
        class Config(SerialDevice.Config): 
            position = TesaNode.Config()

        # make an alias node to correct a value with a linear law 
    class TempCorector(NodeAlias1, offset=(float, 0.0), slope=(float,1.0) ):
        def fget(self, value):
           return value  * self.config.slope + self.config.offset 

    class Sensors(UaDevice):
        class Config(UaDevice.Config):
            raw_temp1: UaNode.Config = UaNode.Config( suffix="lrTemp1" )
            raw_temp2: UaNode.Config = UaNode.Config( suffix="lrTemp2" )
            
            temp1: Defaults[TempCorector.Config] = TempCorector.Config( node = 'raw_temp1' ) 
            temp2: Defaults[TempCorector.Config] = TempCorector.Config( node = 'raw_temp2' )

       
    class MotorSequence(BaseManager):
        class Config( BaseManager.Config ):
            positions: List[float] = [0.0, 1.0]  # gives some default positions
            n_cycle: int = 1
            velocity: float = 3.0 
            
            time: LocalUtcNode.Config = LocalUtcNode.Config()
            tesa: Tesa.Config = Tesa.Config()
            motor: Motor.Config = Motor.Config()
            sensors: Sensors.Config = Sensors.Config()
            
            seq_data: DequeNode.Config = DequeNode.Config( nodes=['time', 'motor.stat.pos_actual', 'motor.stat.pos_error', 'tesa.position', 'sensors.temp1', 'sensors.temp2'] ) 

        class Data(BaseManager.Data): 

            seq_data: NodeVar[list] = []
            last_pos_encoder: NodeVar[float] = Field(0.0, node="motor.stat.pos_actual")
            last_pos : NodeVar[float] = Field(0.0, node="tesa.position")
            temp1: NodeVar[float] = Field(0.0, node="sensors.temp1")
            temp2: NodeVar[float] = Field(0.0, node="sensors.temp2")
        

        
        def connect(self): 
            self.motor.connect()
            self.tesa.connect()
            
        def disconnect(self): 
            self.motor.disconnect()
            self.tesa.disconnect()
        
        def init(self):
            self.motor.configure()
            wait( self.motor.reset() )
            wait( self.motor.ini() )
            wait( self.motor.enable() )
            self.seq_data.reset() # empty the dequeue 

        def run(self, callback= lambda : None):
            for pos in self.config.positions * self.config.n_cycle:
                wait( self.motor.move_abs(pos, self.config.velocity) )
                callback() 

        def save_data(self, data, file): 
           
            with open(file,'w') as g:
                # write data header
                g.write(  "\n".join( self.config.seq_data.nodes  ) )
                # write data
                for l in data.seq_data:
                    g.write( ", ".join(str(x) for x in l) )

    seq = MotorSequence('', config=cfg)
    data = MotorSequence.Data()
    dl = DataLink( seq, data )
        
    try:
         seq.connect()
         seq.init()
         seq.run( dl.download )
        
    finally:
         seq.save_data(data)
         seq.disconnect()




