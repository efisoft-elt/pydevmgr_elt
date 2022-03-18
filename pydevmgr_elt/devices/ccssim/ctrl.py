from pydevmgr_core import  NodeAlias1, Defaults, NodeVar
from pydevmgr_elt.base import EltDevice,  GROUP
from pydevmgr_elt.base.tools import _inc, enum_group, enum_txt, EnumTool

from enum import Enum
Base = EltDevice.Interface

N = Base.Node # Base Node
NC = N.Config
ND = Defaults[NC] # this typing var says that it is a Node object holding default values 
NV = NodeVar # used in Data 



class CcsSimCtrl(Base):
    class Config(Base.Config):
        temperature: ND = NC(suffix="ctrl.environment.temperature", parser=float)
        pressure: ND = NC(suffix="ctrl.environment.pressure", parser=float)
        humidity: ND = NC(suffix="ctrl.environment.humidity", parser=float)
        lapserate: ND = NC(suffix="ctrl.environment.lapserate", parser=float)
        wavelength: ND = NC(suffix="ctrl.wavelength", parser=float)
        dut: ND = NC(suffix="ctrl.dut", parser=float)

 
    class Data(Base.Data):
        temperature: NV[float] = 0.0
        pressure: NV[float] = 0.0
        humidity: NV[float] = 0.0
        lapserate: NV[float] = 0.0
        wavelength: NV[float] = 0.0
        dut: NV[float] = 0.0    



