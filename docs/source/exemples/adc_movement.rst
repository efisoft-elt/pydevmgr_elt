Realistic Adc Movement
======================

Again an tutorial example base on a real need. An ADC hardware is being tested for aging, tracking speed, etc ...

The ESO FCS is not integrated for this test being used in an other institute so pydevmgr_elt comes handy. 


For this tutorial we considers: 
    
    - A PLC Project with   1 ADC, A CcsSim and a Timer instanced
    - They are two REAL values one the PLC to be read directly on the PLC (temperatures), not included in an IODEV
    - We want to be abble to send the ADC in a realistic trajectory 


Main Device
===========

As everything appear on the same PLC we can start from a UaDevice instead of e UaManger or EltManager as it is done 
in the :ref:`A Sequence and measurement Script`. 
The advantage is that OPC-UA communication parameters are entered in one single place. A  "Child" device will share 
the same OPC-UA client than its master (so address, namespace, ... of a child device will be ignored). 

Here is the script:

.. code-block:: python

    from pydevmgr_elt import Adc, CcsSim, Time, NodeVar, DataLink, wait, AllTrue
    from pydevmgr_ua import UaDevice, UaNode
    from pydantic import BaseModel, Field, AnyUrl 
    from datetime import datetime 
    import time
    from typing import List

    # create some scripts configuration 
    class TrackTargetConfig(BaseModel, extra="forbid", validate_assignment=True):
       """ config for one target """
       start_time: datetime = datetime(2027, 1, 1) # A ISO date time format string is also valid     
       end_time:  datetime = datetime(2027, 1, 1, 1) 
       ra: float = 000000.00 
       dec: float = 000000.00
       equinox: float = 2000.0
       name: str = "" # guive some target name for reference 

    class Main(UaDevice):
        class Config(UaDevice.Config): 
           prefix = "MAIN" # this will most probably run on the PLC program named "MAIN" 
           address: AnyUrl = "opc.tcp://myplc.local:4840" # gives some default address
           
           # Add some devices
           adc : Adc.Config = Adc.Config(prefix="adc") # the 'MAIN' is not needed, it will comes from parent device
           ccs : CcsSim.Config = CcsSim.Config(prefix="ccs")
           time : Time.Config = Time.Config(prefix="timer")
           
           # we can add temperatures nodes 
           temp1 : UaNode.Config = UaNode.Config( suffix="lrTemp1")
           temp2:  UaNode.Config = UaNode.Config( suffix="lrTemp2")
           
           # maybe a list of real child device to be used, only the adc in sour case but some other can come later
           devices: List[str] = ['adc'] 
        
           
           # Add some targets for scripting with a default dummy one for demo purpose
           targets : List[TrackTargetConfig] =  [TrackTargetConfig(
                                                    name="dummy", 
                                                    start_time="2032-09-11T01:00:00.0000", 
                                                    end_time="2032-09-11T01:30:00.0000", 
                                                    ra = 163553.00,  dec = -281258.00
                                                )]
           # a time period to fetch data while tracking
           data_period: float = 1.0 # second 
        
        # Add a Data Class for the interested data to be updated 
        # several Data Class can be created function to what kind of script is started 
        class Data(UaDevice.Data):
            adc_mot1_pos: NodeVar[float] = Field(0.0, node="adc.motor1.stat.pos_actual")
            adc_mot2_pos: NodeVar[float] = Field(0.0, node="adc.motor2.stat.pos_actual")
            temp1: NodeVar[float] = 0.0 # no need to define the node path in this case 
            temp2: NodeVar[float] = 0.0
            time: NodeVar[datetime] = Field( datetime(1950, 1, 1), node="time.stat.utc_datetime")
            alt : NodeVar[float] = Field(0.0, node="ccs.stat.alt_deg")
            az  : NodeVar[float] = Field(0.0, node="ccs.stat.az_deg")
            # ETC ......
            target_name: str = ""
            
            def swrite(self):
                # To be customized of course 
                return f"{self.time.isoformat()}  {self.adc_mot1_pos:.3f}  {self.adc_mot2_pos:.3f} {self.alt:.4f}  {self.az:.4f}"
        
        # Concatenate actions (okay this is not very usefull because only one ADC
        # The AllTrue is a node alias and needed for wait function input
        @property
        def devices(self):
            return [getattr(self, name) for name in self.config.devices]
        
        def init(self):
            return AllTrue('is_all_initialised', nodes= [d.init() for d in self.devices] )
        
        def enable(self):
            return AllTrue('is_all_enable',  nodes= [d.enable() for d in self.devices] )
        
        def disable(self):
            return AllTrue('is_all_disable',  nodes= [d.disable() for d in self.devices] )

        def reset(self):
            return AllTrue('is_all_reseted',  nodes= [d.reset() for d in self.devices] )
        
        def configure(self):
            for d in self.devices:
                d.configure()
        

        def run_target_sequence(self):
            
            # configure devices (adc) 
            self.configure()
            # reset and init 
            wait( self.reset()  )
            wait( self.init()   )
            wait( self.enable() )

            
            data = self.Data()
            dl = DataLink(self, data)
            

            def callback():
                dl.download()
                print( data.swrite()) # do something clever here, like writing in a file for instance ploting etc ...
            

            for target in self.config.targets:
                data.target_name = target.name 
                
                self.track_target(target.start_time, target.end_time, 
                                 target.ra, target.dec, target.equinox,
                                 period=self.config.data_period, 
                                 callback=callback
                                 )
         

        
        def track_target(self, start_time, end_time, ra, dec, equinox=2000, period =1, callback=lambda :None):
            self.time.set_time(start_time)
            self.ccs.set_coordinates( ra, dec, equinox)
            
            wait( self.adc.start_track() ) # changing coordinate will send ADC in preset, wait for tracking 
             
            

            while data.time < end_time:
               tic = time.time()
               callback()
               tac= time.time()
               time.sleep( max( period-(tac-tic), 0.001)  ) 


This exemple can than be ran from a configuration file as defined by ``Main.Config``: 

.. code-block:: yaml

    targets: 
        - name: Target1 
          ra: 163553.00
          dec: -281258.00
          start_time: 2032-09-11T01:00:00.0000
          end_time: 2032-09-11T01:30:00.0000
        - name: Target2 
          ra: 171303.0
          dec: -545107.0
          start_time: 2032-09-11T01:30:00.0000
          end_time: 2032-09-11T02:00:00.0000


Or you can configure more deeply, e.i. if you want to check the influance of the init function for instance

.. code-block:: yaml
    targets: 
        - name: Target1 
          ra: 163553.00
          dec: -281258.00
          start_time: 2032-09-11T01:00:00.0000
          end_time: 2032-09-11T01:30:00.0000
        - name: Target2 
          ra: 171303.0
          dec: -545107.0
          start_time: 2032-09-11T01:30:00.0000
          end_time: 2032-09-11T02:00:00.0000

    data_period: 0.5
    
    adc:
        ctrl_config:
            axes: [motor1, motor2]
        motor1:
            type: Motor # mendatory  
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



