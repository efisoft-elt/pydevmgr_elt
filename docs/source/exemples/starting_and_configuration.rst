Get Started & configuration
===========================

This short tutorial is to show you how to use a standard device with pydevmgr with the exempl of a Motor. 


Loading a Motor object
----------------------

Without the need of a configuration file one can simply use the Motor as it is configured on the PLC directly. 
We simplely needs the address and the prefix of the motor inside the PLC (and eventualy the namespace number which is 4
by default). 

.. code-block:: python

   from pydevmgr_elt import Motor, wait

   motor = Motor('my_motor',  address="opc.tcp://myplc.local:4840", prefix="MAIN.Motor1")

   try:
        # Connect the opc-ua client (inside the motor instance) to the opc-ua server (PLC)
        motor.connect() 
        
        # Reset and initialise the motor 
        wait( motor.reset() ) 
        wait( motor.init() )
        wait( motor.enable() )
        
        # move to a given position 
        wait( motor.move_abs( 5.0, 1.0 ) ) # pos, velocity 
        
        print( "Motor is at ", motor.stat.pos_actual.get() )
    finally:
        # Donne with the motor or an error occured 
        # we can close the opc-ua socket connection so script is ending nicely 
        motor.disconnect()
    

Using a configuration file 
--------------------------

The shortest way to use a configuration file is tu use the :func:`pydevmgr_elt.open_elt_device`. 
So far pydevmgr_elt is compatible with the configuration file defined by ESO as for v3 of IFW. 

.. code-block:: python

   from pydevmgr_elt import open_elt_device

   motor = open_elt_device('tins/motor1.yml')

The path to the configuration file can be either absolute (e.g. ``/users/me/resources/motor1.yml``) or relative to 
one of the path defined in the $CFGPATH environment variable (e.g. ``export CFGPATH=${HOME}/resources1:${HOME}/resources2`` )

Note that the configuration file have some  configuration which are supposed to be send to the PLC, they overwrite the
PLC current configuration. One need to do this manually, so if you want to execute a script with exactly the same motor
configuration (true for other devices of course) you need to execute the ``.confugure()`` function 

.. code-block:: python 

   from pydevmgr_elt import open_elt_device

   motor = open_elt_device('tins/motor1.yml')
   
   try:
        motor.connect()
        #  transfer the init sequence and other ctrl_config parameters to the PLC
        motor.configure() 
        wait( motor.reset() )
        wait( motor.init()  )
        # etc ...
    finally:
        motor.disconnect()


A bit of a mix 
--------------

You may not want to use a configuration file but configure the motor inside the script. They are two ways to do it 
first you can edit the config object and than use the ``.configure()`` method : 

.. code-block:: python

   from pydevmgr_elt import Motor

   motor = Motor( 'motor', address="opc.tcp://my-plc.local:4840", prefix="MAIN.Motor1",
                ctrl_config=Motor.Config.CtrlConfig(
                    velocity = 3.0, 
                    min_pos = 0.0, 
                    max_pos = 10.0, 
                    axis_type = "LINEAR", 
                    backlash = 0.02, 
                    # etc ....
                               
                ), 
                initialisation = Motor.Config.Initialisation(
                    sequence = ['FIND_LHW', 'CALIB_ABS', 'END'], 
                    FIND_LHW = {'value1': 1.0, 'value2': 0.2}, 
                    CALIB_ABS = {'value1': 0.0}
                )
            )


Or you can use a dictionary for configuration. Or as I like to do is writing directly the yml in your script: 

.. code-block:: python 
    
    from pydevmgr_elt import Motor
    import yaml 
    cfg = yaml.load("""
      type: Motor
      prefix: MAIN.Motor1
      ignored: false
      address: opc.tcp://myplc.local:4840
      fits_prefix: "MOT1"
      ctrl_config:
        velocity:              3.0
        min_pos:               0.0
        max_pos:               359.0
        axis_type:             CIRCULAR
        active_low_lstop:      false
        active_low_lhw:        false
        active_low_ref:        true
        active_low_index:      false
        active_low_uhw:        true
        active_low_ustop:      false
        brake:                 false
        low_brake:             false
        low_inpos:             false
        backlash:              0.0
        tout_init:             30000
        tout_move:             120000
        tout_switch:           10000
      initialisation:
          sequence: ['FIND_LHW', 'FIND_UHW', 'CALIB_ABS', 'END']
          FIND_LHW:
             value1: 4.0
             value2: 4.0
          FIND_UHW:
             value1: 4.0
             value2: 4.0
          CALIB_ABS:
             value1: 0.0
             value2: 0.0
          END:
             value1: 0.0
             value2: 0.0
      positions:
         posnames: ['ON', 'OFF']
         "ON": 30
         "OFF": 100
    """, Loader=yaml.CLoader)
    
    motor = Motor('motor' , config=cfg)


The confguration values are parsed at creation, you can try to make, for instance an error in the address 

.. code-block:: python
   
   from pydevmgr_elt import Motor
    
   config = Motor.Config( address="opc.tcp///127.0.0.1:4840" )
   #ValidationError: 1 validation error for Motor.Config
   #     address
   #invalid or missing URL scheme (type=value_error.url.scheme)
