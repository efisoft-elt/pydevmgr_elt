from pydevmgr_core import   NodeVar, set_data_model
from pydevmgr_elt.base import EltDevice

Base = EltDevice.Interface

N = Base.Node # Base Node
NC = N.Config
NV = NodeVar # used in Data 


@set_data_model
class CcsSimCtrl(Base):
    class Config(Base.Config):
        temperature: NC = NC(suffix="ctrl.environment.temperature", vtype=(float, 20.0), parser=float)
        pressure: NC = NC(suffix="ctrl.environment.pressure", vtype=(float, 760.0), parser=float)
        humidity: NC = NC(suffix="ctrl.environment.humidity", vtype=(float, 50.0), parser=float)
        lapserate: NC = NC(suffix="ctrl.environment.lapserate", vtype=(float, 0.0065), parser=float)
        wavelength: NC = NC(suffix="ctrl.wavelength", vtype=(float, 600.0), parser=float)
        dut: NC = NC(suffix="ctrl.dut", vtype=float, parser=float)

        alpha :    NC= NC(suffix="ctrl.meanCoordinates.alpha", vtype=float, parser=float)
        delta :    NC= NC(suffix="ctrl.meanCoordinates.delta", vtype=float, parser=float)
        epoch :    NC= NC(suffix="ctrl.meanCoordinates.epoch", vtype=float, parser=float)
        equinox :  NC= NC(suffix="ctrl.meanCoordinates.equinox", vtype=(float,2000.0),  parser=float)
        pma :      NC= NC(suffix="ctrl.meanCoordinates.pma", vtype=float, parser=float)
        pmd :      NC= NC(suffix="ctrl.meanCoordinates.pmd", vtype=float, parser=float)
        radvel :   NC= NC(suffix="ctrl.meanCoordinates.radvel", vtype=float, parser=float)
        parallax : NC= NC(suffix="ctrl.meanCoordinates.parallax", vtype=float, parser=float)
        
        motion_x :   NC= NC(suffix="ctrl.motion.x", vtype=float, parser=float)
        motion_y :  NC= NC(suffix="ctrl.motion.y", vtype=float, parser=float)


        
