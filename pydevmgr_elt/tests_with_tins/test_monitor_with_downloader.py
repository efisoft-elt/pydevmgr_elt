import time
from pydevmgr_elt import Motor, nodes, BaseMonitor, NodeVar, wait, Downloader
from pydevmgr_core import signals 


from pydantic import Field 
from matplotlib.pylab import plt 



class Monitor(BaseMonitor):

    class Data(BaseMonitor.Data):
        pos : NodeVar[float] = Field(0.0, node="stat.pos_actual")
        vel : NodeVar[float] = Field(0.0, node="stat.vel_actual")
        time: NodeVar[float] = Field(0.0, node= nodes.ElapsedTime())

        direction: int = +1    
        nstep: int = 0
        attempt_counter: int = 0
        
    class Config(BaseMonitor.Config):
        velocity: float = 1.0
        min: float = 0.0 
        max: float = 5.0
        max_step: int = 2 

    def start(self, motor: Motor, data: Data):
        print( "Hello I am starting")
        wait(motor.reset())
        wait(motor.init()) 
        wait(motor.enable()) 
        
        motor.move_vel(data.direction * self.config.velocity)
        data.nstep = 1    


    def next(self, motor, data):
        data.direction = -data.direction
        motor.move_vel(data.direction * self.config.velocity)
        data.nstep += 1
        
    def update( self, data):
        if data.nstep > self.config.max_step:
            raise self.StopMonitor
        print(data.time, data.pos )
        if (data.pos>self.config.max and data.direction>0) or  (data.pos<self.config.min and data.direction<0.0): 
            raise self.NextSetup
    
    def update_failure(self, data, err):
        if err:
            if data.attempt_counter>10:
                data.attempt_counter = 0
                raise self.StopMonitor
            else:
                data.attempt_counter += 1
                print("Failure in updating data ", data.attempt_counter, flush=True)
        else:
            data.attempt_counter = 0 

    def end(self, device, data, error):
        device.stop()
        print( "this is the end") 


if __name__ == "__main__":

       with Motor( address="opc.tcp://192.168.1.11:4840", prefix="MAIN.Motor1") as motor:
           downloader = Downloader()
           
           connector = Monitor().connector( motor)

           connector.connect(downloader)
           downloader.run(period=0.5, stop_signal=signals.Timeout(10.0))
           
       

    
