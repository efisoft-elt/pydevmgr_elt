from pydevmgr_core import   NodeVar
from pydevmgr_core.base.dataclass import set_data_model
from pydevmgr_ua.uainterface import UaInterface
from pydevmgr_elt.base import EltDevice  
from enum import Enum 
from pydevmgr_elt.devices.time.stat import MODE
Base = EltDevice.Interface

N = Base.Node # Base Node
NC = N.Config
NV = NodeVar # used in Data 


class SOURCE(int, Enum):
    NONE = 0
    NTP = 1
    PTP = 2


@set_data_model
class DiagReport(UaInterface):
    class Config:
        enabled: NC = NC( suffix="enabled", vtype=bool)
        address: NC = NC( suffix="address", vtype=str)
        destination_port: NC = NC(suffix="destination_port", vtype=int)
        source_port: NC = NC(suffix="source_port", vtype=(int, 10000))

        topic_id: NC = NC(suffix="topic_id", vtype=(int,500))
        component_id: NC = NC(suffix="compontent_id", vtype=(int,1))
        sampling: NC = NC(suffix="sampling", vtype=(int, 10000))
        



# Nothing to declare cfg is empty 
@set_data_model
class TimeCfg(Base):
    class Config(Base.Config):

        mode :NC = NC( suffix="cfg.nMode", vtype=(MODE, MODE.LOCAL), output_parser=MODE)
        source: NC =NC( suffix="cfg.nSource", vtype=(SOURCE,SOURCE.NONE),output_parser=SOURCE)  
        user_time_string: NC = NC(suffix="cfg.sUserTime", vtype=(str, 'YYYY-MM-DD-hh:mm:ss.nnnnnnnnn'))
        user_time: NC = NC(suffix="cfg.tUserTime", vtype=int)
        leap: NC = NC(suffix="cfg.nLeapSecond", vtype=int, unit="s")
        
        report = DiagReport.Config(prefix="cfg.diag_report")   

