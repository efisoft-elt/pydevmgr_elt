from pydevmgr_core import NodeAlias, buildproperty, NodeVar, record_class, BaseDevice

from ..base.eltdevice import EltDevice, GROUP

from ..base.tools import  _inc, enum_group, enum_txt, EnumTool
from pydevmgr_ua import Int32,  UInt32, UaNode, UaRpc, UaInterface

import datetime

from pydantic import BaseModel
from enum import Enum

from typing import Optional, Union 

class TimeCtrlConfig(EltDevice.Config.CtrlConfig):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    latitude  : Optional[float] = -0.429833092 
    longitude : Optional[float] = 1.228800386

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
class TimeConfig(EltDevice.Config):
    CtrlConfig = TimeCtrlConfig
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ctrl_config : CtrlConfig = CtrlConfig() 
    type: str = "Time"
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
#                      _              _   
#   ___ ___  _ __  ___| |_ __ _ _ __ | |_ 
#  / __/ _ \| '_ \/ __| __/ _` | '_ \| __|
# | (_| (_) | | | \__ \ || (_| | | | | |_ 
#  \___\___/|_| |_|___/\__\__,_|_| |_|\__|
# 
##### ###########
# SUBSTATE
class MODE(EnumTool, int, Enum):
    LOCAL                  =   0    
    UTC                    =   1
    SIMULATION             =   2
    
    UNREGISTERED = -9999

class STATUS(EnumTool, int, Enum):
    CONNECTED = 0
    NOT_CONNECTED = 1

class QOS(EnumTool, int, Enum):
    NOT_VALID = 0
    NOT_SYNCHRONIZED = 1
    VALID = 2


class RPC_ERROR(EnumTool, int, Enum):
    OK = 0
    NO_SIMULATION_MODE = 1
    DC2TC_OFFSET_NOT_MAPPED = 2
    INT_EXT_NOT_MAPPED = 3
    COE_NOT_VALID = 4 
    PTP_WRONG_STATE = 5
    PTP_NOT_SYNCHRONIZED = 6

enum_txt ( {
   RPC_ERROR.OK:					 'OK',
   RPC_ERROR.NO_SIMULATION_MODE:	    'ERROR: Time can only be set in simulation mode.',	
   RPC_ERROR.INT_EXT_NOT_MAPPED:        'ERROR: Did you forgot to map the internal or external EL6688 time stamps?',
   RPC_ERROR.DC2TC_OFFSET_NOT_MAPPED:   'ERROR: Did you forgot to map the dc2tc_offset?',
   RPC_ERROR.COE_NOT_VALID:             'ERROR: Error reading COE parameter',
   RPC_ERROR.PTP_WRONG_STATE:           'ERROR: EL6688 is not in SLAVE state',
   RPC_ERROR.PTP_NOT_SYNCHRONIZED:      'WARNING: PTP not synchronized',
})

#  ____        _          __  __           _      _ 
# |  _ \  __ _| |_ __ _  |  \/  | ___   __| | ___| |
# | | | |/ _` | __/ _` | | |\/| |/ _ \ / _` |/ _ \ |
# | |_| | (_| | || (_| | | |  | | (_) | (_| |  __/ |
# |____/ \__,_|\__\__,_| |_|  |_|\___/ \__,_|\___|_|
# 

class TimeCfgData(BaseDevice.Data):
    pass
  
class TimeStatData(BaseDevice.Data):
    dc_time : NodeVar[str] = "" 
    utc_time : NodeVar[str] = "" 
    tai_time : NodeVar[str] = "" 
    error_msg : NodeVar[str] = "" 
    mode :  NodeVar[int] = 0
    mode_txt :  NodeVar[str] = ""
    
    ptp_offset_time : NodeVar[int] = 0 
    sim_offset_time : NodeVar[int] = 0 
    dc_time_int     : NodeVar[int] = 0 
    utc_time_int    : NodeVar[int] = 0 
    tai_time_int    : NodeVar[int] = 0 
    tai_unix_time   : NodeVar[int] = 0 
    
    
    user_time : NodeVar[str] = "" 
    user_time_int : NodeVar[int] = 0 
    status :  NodeVar[int] = 0 
    status_txt : NodeVar[str] = ""
     
    qos: NodeVar[int] = 0 
    qos_txt: NodeVar[str] = 0 
    time_difference: NodeVar[int] = 0
    
class TimeData(BaseDevice.Data):
    StatData = TimeStatData
    CfgData = TimeCfgData
        
    cfg: CfgData = CfgData()
    stat: StatData = StatData()    


def isodate(d: Union[str,datetime.datetime]):
    """ parse an input datetime or iso string to a string of fomat '2021-04-26-09:23:54.142136' """
    if isinstance(d, datetime.datetime):
        return  d.isoformat().replace("T", "-") 
    return d.replace("T", "-") 


#  _       _             __                
# (_)_ __ | |_ ___ _ __ / _| __ _  ___ ___ 
# | | '_ \| __/ _ \ '__| |_ / _` |/ __/ _ \
# | | | | | ||  __/ |  |  _| (_| | (_|  __/
# |_|_| |_|\__\___|_|  |_|  \__,_|\___\___|

class TimeStatInterface(UaInterface):
    Data = TimeStatData
    MODE = MODE
    QOS = QOS
    fits_key = ""
    @NodeAlias.prop("time", ["mode", "utc_time", "dc_time"])
    def time(self, mode: int, utc:str, dc:str) -> str:        
        """ Return a text representation of the mode """
        return dc if mode == self.MODE.LOCAL else utc 
            
    @NodeAlias.prop("mode_txt", ["mode"])
    def mode_txt(self, mode: int) -> str:
        """ Return a text representation of the mode """
        return self.MODE(mode).txt
    
    @NodeAlias.prop("qos_txt", ["qos"])
    def qos_txt(self, qos: int) -> str:
        """ Return a text representation of the qos """
        return self.QOS(qos).txt
        
    @NodeAlias.prop("status_txt", ["status"])
    def status_txt(self, status: int) -> str:
        """ Return a text representation of the status """
        return self.QOS(status).txt    

class TimeCfgInterface(UaInterface):
    # we can define the type to parse value directly on the class by annotation
    Data = TimeCfgData
    
@buildproperty(UaRpc.prop, 'args_parser') 
class TimeRpcInterface(UaInterface):  
    RPC_ERROR = RPC_ERROR  
    rpcSetTime : (str,)
    rpcSetMode : (Int32,)
    


#      _            _          
#   __| | _____   _(_) ___ ___ 
#  / _` |/ _ \ \ / / |/ __/ _ \
# | (_| |  __/\ V /| | (_|  __/
#  \__,_|\___| \_/ |_|\___\___|
#


@record_class
class Time(EltDevice):    
    MODE = MODE
    STATUS = STATUS
    
    Config = TimeConfig
    Data = TimeData
    
    StatInterface = TimeStatInterface
    CfgInterface = TimeCfgInterface
    RpcInterface = TimeRpcInterface
    
                
    stat = StatInterface.prop('stat')    
    cfg  = CfgInterface.prop('cfg')
    rpc  = RpcInterface.prop('rpc')
    
    def reset(self) -> UaNode:
        raise ValueError('Time has no reset capability')

    def enable(self) -> UaNode:
        raise ValueError('Time has no enable capability')
        
    def disable(self) -> UaNode:
        raise ValueError('Time has no disable capability')
    
    def init(self) -> UaNode:
        raise ValueError('Time has no init capability')
    
    def set_mode(self, mode: int) -> None:
        mode = int(self.MODE(mode)) # this will raise error if mode is incorrect 
        self.rpc.rpcSetMode.rcall(mode)
        
    def set_time(self, time: Union[str,datetime.datetime, None]) -> None:
        """ Set time to PLC. If None time will be datetime.now() 
        
        Before setting time the mode is automaticaly switched to simulation 
        """        
        time = isodate(datetime.datetime.now() if time is None else time)
        self.set_mode(MODE.LOCAL) # patch to clear any error 
        self.set_mode(MODE.SIMULATION)
        self.rpc.rpcSetTime.rcall(time)        



