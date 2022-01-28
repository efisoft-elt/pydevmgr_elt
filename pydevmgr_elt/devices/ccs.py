from pydevmgr_core import NodeAlias, buildproperty, NodeVar, upload, record_class, upload
from ..base.eltdevice import (EltDevice, GROUP)
from pydevmgr_ua import (Int32, UInt32)
from ..base.tools import  _inc, enum_group, enum_txt, EnumTool

from pydantic import BaseModel
from enum import Enum

from typing import Optional

class CcsSimCtrlConfig(EltDevice.Config.CtrlConfig):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    latitude  : Optional[float] = -0.429833092 
    longitude : Optional[float] = 1.228800386

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
class CcsSimConfig(EltDevice.Config):
    CtrlConfig = CcsSimCtrlConfig
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ctrl_config : CtrlConfig = CtrlConfig() 
    type: str = "CcsSim"
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
#                      _              _   
#   ___ ___  _ __  ___| |_ __ _ _ __ | |_ 
#  / __/ _ \| '_ \/ __| __/ _` | '_ \| __|
# | (_| (_) | | | \__ \ || (_| | | | | |_ 
#  \___\___/|_| |_|___/\__\__,_|_| |_|\__|
# 
##### ###########
# SUBSTATE
class TIME_MODE(EnumTool, int, Enum):
    LOCAL                  =   0    
    UTC                    =   1
    
    UNREGISTERED = -9999





#  ____        _          __  __           _      _ 
# |  _ \  __ _| |_ __ _  |  \/  | ___   __| | ___| |
# | | | |/ _` | __/ _` | | |\/| |/ _ \ / _` |/ _ \ |
# | |_| | (_| | || (_| | | |  | | (_) | (_| |  __/ |
# |____/ \__,_|\__\__,_| |_|  |_|\___/ \__,_|\___|_|
# 

class CcsSimCfgData(EltDevice.Interface.Data):
    latitude:  NodeVar[float] =  -0.429833092     
    longitude:  NodeVar[float] = 1.228800386    
  
class CcsSimCtrlData(EltDevice.Interface.Data):
    temperature: NodeVar[float] = 0.0
    pressure: NodeVar[float] = 0.0
    humidity: NodeVar[float] = 0.0
    lapserate: NodeVar[float] = 0.0
    wavelength: NodeVar[float] = 0.0
    dut: NodeVar[float] = 0.0    
      
class CcsSimStatData(EltDevice.Interface.Data):
    time_mode: NodeVar[int] = 0
    sdc_time: NodeVar[str]  = ""
    dc_time : NodeVar[int] = 0  
    
    apparent_alpha: NodeVar[float] = 0.0 
    apparent_delta: NodeVar[float] = 0.0 
    alpha :  NodeVar[float]  = 0.0 
    delta :  NodeVar[float]  = 0.0 
    ha :  NodeVar[float]  = 0.0  
    zd :  NodeVar[float]  = 0.0  
    az :  NodeVar[float]  = 0.0 
     
    
    temperature: NodeVar[float]  = 0.0  
    pressure: NodeVar[float]     = 0.0     
    humidity: NodeVar[float]     = 0.0     
    lapserate: NodeVar[float]    = 0.0    
    
    lst : NodeVar[float] = 0.0
    pa  : NodeVar[float] = 0.0
    pa_deg : NodeVar[float] = 0.0
    alt : NodeVar[float] = 0.0
    alt_deg : NodeVar[float] = 0.0
    ha: NodeVar[float] = 0.0
    az: NodeVar[float] = 0.0
    az_deg : NodeVar[float] = 0.0
    rotation: NodeVar[float] = 0.0
    rotation_deg : NodeVar[float] = 0.0
    ra: NodeVar[float] = 0.0
    dec: NodeVar[float] = 0.0
    
class CcsSimData(EltDevice.Data):
    StatData = CcsSimStatData
    CfgData = CcsSimCfgData
        
    cfg: CfgData = CfgData()
    stat: StatData = StatData()    


#  _       _             __                
# (_)_ __ | |_ ___ _ __ / _| __ _  ___ ___ 
# | | '_ \| __/ _ \ '__| |_ / _` |/ __/ _ \
# | | | | | ||  __/ |  |  _| (_| | (_|  __/
# |_|_| |_|\__\___|_|  |_|  \__,_|\___\___|
@record_class
class CcsSimStatInterface(EltDevice.Interface):
    class Config(EltDevice.StatInterface.Config):
        type: str = 'CcsSim.Stat'
    Data = CcsSimStatData
    
    TIME_MODE = TIME_MODE
    
    @NodeAlias.prop("time_mode_txt", ["time_mode"])
    def time_mode_txt(self, time_mode: int) -> str:
        """ Return a text representation of the time_mode """
        return self.TIME_MODE(time_mode).txt
    
@record_class    
@buildproperty(EltDevice.Node.prop, 'parser')      
class CcsSimCfgInterface(EltDevice.Interface):
    class Config(EltDevice.CfgInterface.Config):
        type: str = 'CcsSim.Cfg'
    Data = CcsSimCfgData
    # we can define the type to parse value directly on the class by annotation
    latitude:   float
    longitude:  float
    
@record_class
@buildproperty(EltDevice.Node.prop, 'parser')      
class CcsSimCtrlInterface(EltDevice.Interface):
    class Config(EltDevice.RpcInterface.Config):
        type: str = 'CcsSim.Rpc'
    # we can define the type to parse value directly on the class by annotation
    temperature: float
    pressure: float
    humidity: float
    lapserate: float
    wavelength: float
    dut: float




@buildproperty(EltDevice.Rpc.prop, 'args_parser') 
class CcsSimRpcInterface(EltDevice.Interface):   
    Data = CcsSimCtrlData 
    rpcSetCoordinates : (float, float, float)


#      _            _          
#   __| | _____   _(_) ___ ___ 
#  / _` |/ _ \ \ / / |/ __/ _ \
# | (_| |  __/\ V /| | (_|  __/
#  \__,_|\___| \_/ |_|\___\___|
#
@record_class
class CcsSim(EltDevice):    
    
    Config = CcsSimConfig
    Data = CcsSimData
    
    StatInterface = CcsSimStatInterface
    CfgInterface = CcsSimCfgInterface
    RpcInterface = CcsSimRpcInterface
    
                
    stat = StatInterface.prop('stat')    
    cfg  = CfgInterface.prop('cfg')
    rpc  = RpcInterface.prop('rpc')
    
    def reset(self) -> EltDevice.Node:
        raise ValueError('CcsSim has no reset capability')

    def enable(self) -> EltDevice.Node:
        raise ValueError('CcsSim has no enable capability')
        
    def disable(self) -> EltDevice.Node:
        raise ValueError('CcsSim has no disable capability')
    
    def init(self) -> EltDevice.Node:
        raise ValueError('CcsSim has no init capability')
    
    def set_coordinates(self, ra: float, dec: float, equinox: float) -> None:
        self.rpc.rpcSetCoordinates.rcall(ra, dec, equinox)
    
    def set_environment(self, 
            temperature: Optional[float] = None, 
            pressure: Optional[float] =None, 
            humidity: Optional[float] =None, 
            lapserate: Optional[float] =None, 
            wavelength: Optional[float] = None, 
            dut: Optional[float] = None                              
        ):
        """ set environmnent data to the CCS Simulator 
        
        Each settings arguments are potional: 
          temperature, pressure, humidity, lapserate, wavelength, dut   
        
        """
        nodes = {}
        if temperature is not None:
            nodes[self.ctrl.temperature] = temperature
        
        if pressure is not None:
            nodes[self.ctrl.pressure] = pressure
        
        if humidity is not None:
            nodes[self.ctrl.humidity] = humidity
            
        if lapserate is not None:
            nodes[self.ctrl.lapserate] = lapserate    
        
        if wavelength is not None:
            nodes[self.ctrl.wavelength] = wavelength 
        
        if dut is not None:
            nodes[self.ctrl.dut] = dut        
        upload(nodes)          
        

