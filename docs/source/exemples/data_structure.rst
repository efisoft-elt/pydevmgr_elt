Retrieving data in structure
============================

In this tutorial we will see how to use data models (pydantic models) to retrieve information on the PLC for any
applications. 

In pydevmgr_elt the data is completly separated to the engine to retrieve data from server. For instance 
in a  :class:`pydevmgr_elt.Motor` class their is no last_data or default_data or whatsoever in the Motor nodes. 

Native Data structure
---------------------

The devices have all a Data class attached, this Data class can be instancied and use normaly : 

.. code-block:: python 

   from pydevmgr_elt import Motor

   data = Motor.Data()

   data.stat.pos_actual 
   # 0.0
   data.stat.substate
   # 0

At creation the data is filled with default values, one need to link the data to a motor instance with a
:class:`pydevmgr_elt.DataLink`. A call of the ``.download`` method will fill the data field to live values from the
OPC-UA 

.. code-block:: python 

   from pydevmgr_elt import Motor, DataLink

   motor = Motor('my_motor',  address="opc.tcp://myplc.local:4840", prefix="MAIN.Motor1")
   data = Motor.Data()

   data_link = DataLink( motor, data )
   
   try:
        # need to connect the opc-ua client
        motor.connect()
        
        # This will update all values of data from the OPC-UA
        data_link.download()
        
        print( f"motor is at {data.stat.pos_actual}mm wit a position error of {data.stat.pos_error}") 
        print( f"the configured backlash is  {data.cfg.backlash}" )
    
    finally:
        motor.disconnect()


This is a great way to separate the function/application dealing with the data informations (plot, logging, gui,
tunning, ... ) to the way to retrieve it. 

Note that the `.download` method of the data_link will ask node values in one single OPC-UA call. 

If you are dealing with several Data classes you can add them to a Downloader : 

.. code-block:: python

   from pydevmgr_elt import Motor, Lamp, DataLink, Downloader
   
   motor = Motor('my_motor',  address="opc.tcp://myplc.local:4840", prefix="MAIN.Motor1")
   lamp = Lamp('my_lamp',  address="opc.tcp://myplc.local:4840", prefix="MAIN.Lamp1") 
   
   motor_data = Motor.Data()
   lamp_data = Lamp.Data()
   
   downloader.add_datalink(..., DataLink(motor, motor_data))
   downloader.add_datalink(..., DataLink(lamp, lamp_data))

   try:
    
        motor.connect()
        lamp.connect()
        
        # tHe following will update the motor_data and the lamp_data in one single call 
        downloader.download()
        my_function_using_data( motor_data, lamp_data )
    finally:
        
        motor.disconnect()
        lamp.disconnect()


Manager
-------

Actually the exemple above can be simplified if one use a :class:`pydevmgr_elt.EltManager`. the manager is used to
concatenate some action and can create a Data class from available devices.   


.. code-block:: python

    from pydevmgr_elt import EltManager, Motor, Lampo, DataLink, wait
     
    devices = dict(
        motor =  Motor(address="opc.tcp://myplc.local:4840", prefix="MAIN.Motor1"),
        lamp = Lamp('my_lamp',  address="opc.tcp://myplc.local:4840", prefix="MAIN.Lamp1") 
    )

    m = EltManager( 'fcs', devices=devices)
    
    Data = m.create_data_class()
    data = Data()
    data_link = DataLink(m , data)
    

    try:
        # connect all devices
        m.connect()
        # init all devices 
        wait( m.reset() )
        wait( m.init() )
        wait( m.enable() )
        
        data_link.download()

        print( "Motor is at",  data.motor.stat.pos_actual )
    finally:
        # diconnect all devices
        m.connect()


Custom Data structure
---------------------

The data structure is built from a pydantic model. 

The annotation in the structure indicate the DataLink one a field is refering to a Node, for instance : 

.. code-block:: python 

   from pydevmgr_elt import DataLink, NodeVar
   from pydantic import BaseModel, Field
   
   class MyMotorStatData(BaseModel):
        
        normal_value: int = 0  # a normal value,  ignored by DataLink 
        pos_actual: NodeVar[float] = 0.0
        pos_error: NodeVar[float] = 0.0 

   stat_data = MyMotorStatData()
   motor =  Motor(address="opc.tcp://myplc.local:4840", prefix="MAIN.Motor1")
   dl = DataLink( motor.stat , stat_data )

The exemple above will work because  `pos_error` and `pos_actual` are matching the node name inside `motor.stat`. 
If you wish to change the name or the path inside the data structure you need to use the Field pydantic class with a
node keyword : 


.. code-block:: python 

   from pydevmgr_elt import DataLink, NodeVar
   from pydantic import BaseModel, Field

   class MyMotorData(BaseModel):  
    
        pos: NodeVar[float] = Field(0.0, node="stat.pos_actual")
        err: NodeVar[float] = Field(0.0, node="stat.pos_error")
        backlash: NodeVar[float] = Field(0.0, node="cfg.backlash")

   data = MyMotorData()
   motor =  Motor(address="opc.tcp://myplc.local:4840", prefix="MAIN.Motor1")
   dl = DataLink( motor , data )

   try:
        motor.connect()
        dl.download()
        print( data )

   finally:
        motor.disconnect()
    





