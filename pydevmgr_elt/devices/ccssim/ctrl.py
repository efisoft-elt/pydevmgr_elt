from pydevmgr_core import   NodeVar
from pydevmgr_elt.base import EltDevice

Base = EltDevice.Interface

N = Base.Node # Base Node
NC = N.Config
NV = NodeVar # used in Data 



class CcsSimCtrl(Base):
    class Config(Base.Config):
        temperature: NC = NC(suffix="ctrl.environment.temperature", parser=float)
        pressure: NC = NC(suffix="ctrl.environment.pressure", parser=float)
        humidity: NC = NC(suffix="ctrl.environment.humidity", parser=float)
        lapserate: NC = NC(suffix="ctrl.environment.lapserate", parser=float)
        wavelength: NC = NC(suffix="ctrl.wavelength", parser=float)
        dut: NC = NC(suffix="ctrl.dut", parser=float)

        alpha :    NC= NC(suffix="ctrl.meanCoordinates.alpha", parser=float)
        delta :    NC= NC(suffix="ctrl.meanCoordinates.delta", parser=float)
        epoch :    NC= NC(suffix="ctrl.meanCoordinates.epoch", parser=float)
        equinox :  NC= NC(suffix="ctrl.meanCoordinates.equinox", parser=float)
        pma :      NC= NC(suffix="ctrl.meanCoordinates.pma", parser=float)
        pmd :      NC= NC(suffix="ctrl.meanCoordinates.pmd", parser=float)
        radvel :   NC= NC(suffix="ctrl.meanCoordinates.radvel", parser=float)
        parallax : NC= NC(suffix="ctrl.meanCoordinates.parallax", parser=float)
        
        motion_x :   NC= NC(suffix="ctrl.motion.x", parser=float)
        motion_y :  NC= NC(suffix="ctrl.motion.y", parser=float)


 
    class Data(Base.Data):
        temperature: NV[float] = 0.0
        pressure: NV[float] = 0.0
        humidity: NV[float] = 0.0
        lapserate: NV[float] = 0.0
        wavelength: NV[float] = 0.0
        dut: NV[float] = 0.0    



