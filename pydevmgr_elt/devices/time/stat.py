
from pydantic.config import Extra
from pydevmgr_core import   NodeVar
from pydevmgr_core.base.dataclass import set_data_model
from pydevmgr_core.decorators import nodealias 
from pydevmgr_elt.base import EltDevice
from pydevmgr_elt.base.tools import  get_txt
import datetime
from enum import Enum
from valueparser.parsers import Enumerated 

Base = EltDevice.Interface # not the .Stat
N = Base.Node # Base Node
NC = N.Config
NV = NodeVar # used in Data 
#                      _              _   
#   ___ ___  _ __  ___| |_ __ _ _ __ | |_ 
#  / __/ _ \| '_ \/ __| __/ _` | '_ \| __|
# | (_| (_) | | | \__ \ || (_| | | | | |_ 
#  \___\___/|_| |_|___/\__\__,_|_| |_|\__|
# 

##### ###########
# SUBSTATE
class MODE(int, Enum):
    LOCAL                  =   0   
    UTC_PTP                =   1
    UTC_NTP                =   2
    UTC                    =   3
    SIMULATION             =   4
    
    UNREGISTERED = -9999

class STATUS(int, Enum):
    CONNECTED = 0
    NOT_CONNECTED = 1

class QOS(int, Enum):
    NOT_VALID = 0
    NOT_SYNCHRONIZED = 1
    VALID = 2





    #  ____  _        _     ___       _             __                 
    # / ___|| |_ __ _| |_  |_ _|_ __ | |_ ___ _ __ / _| __ _  ___ ___  
    # \___ \| __/ _` | __|  | || '_ \| __/ _ \ '__| |_ / _` |/ __/ _ \ 
    #  ___) | || (_| | |_   | || | | | ||  __/ |  |  _| (_| | (_|  __/ 
    # |____/ \__\__,_|\__| |___|_| |_|\__\___|_|  |_|  \__,_|\___\___| 

@set_data_model
class TimeStat(Base):
    # Add the constants to this class 
    MODE = MODE
    QOS = QOS
    STATUS = STATUS
    fits_key = ""
    class Config(Base.Config, extra=Extra.forbid):
        # define all the default configuration for each nodes. 
        # e.g. the suffix can be overwriten in construction (from a map file for instance)
        # all configured node will be accessible by the Interface
        dc_time :  NC = NC(suffix="stat.sDcTime", vtype=str)
        utc_time : NC = NC(suffix="stat.sUtcTime", vtype=str)
        tai_time : NC = NC(suffix="stat.sTaiTime", vtype=str)
        error_msg : NC = NC(suffix="stat.sErrorMsg", vtype=str)
        mode :  NC = NC(suffix="stat.mode", vtype=(MODE,MODE.LOCAL), output_parser=MODE)
        ptp_offset_time : NC = NC(suffix="stat.lPtpOffsetTime", vtype=int)
        sim_offset_time : NC = NC(suffix="stat.lSimOffsetTime", vtype=int)
        dc_time_int : NC = NC(suffix="stat.lDcCurrentTime", vtype=int)
        utc_time_int : NC = NC(suffix="stat.lUtcTime", vtype=int)
        tai_time_int : NC = NC(suffix="stat.lTaiTime", vtype=int)
        tai_unix_time : NC = NC(suffix="stat.lTaiUnixTime", vtype=int)
        
    
        user_time : NC = NC(suffix="stat.sUserTime", vtype=str) 
        # STRING(29) := 'YYYY-MM-DD-hh:mm:ss.nnnnnnnnn';
        user_time_int :  NC = NC(suffix="stat.tUserTime", vtype=int) #      ULINT := 0;
        status: NC = NC(suffix="stat.signal.status", vtype=(STATUS,STATUS.NOT_CONNECTED), output_parser=STATUS)
        qos: NC = NC(suffix="stat.signal.qos", vtype=(QOS, QOS.NOT_VALID), output_parser=QOS)
        time_difference : NC = NC(suffix="stat.signal.time_difference" , vtype=int) 
        #: UDINT; // Time difference between DC and External Time Source
    
    @nodealias("mode", "utc_time", "dc_time")
    def time(self, mode: int, utc:str, dc:str) -> str:        
        """ Return a text representation of the mode """
        return dc if mode == self.MODE.LOCAL else utc 
    
    @nodealias("utc_time")
    def utc_datetime(self, utc):
        """ Convert the UTC returned by timer (which is not ISO) to a datetime 
        
        The returned datetime object is at nanosec precision 
        """
        return datetime.datetime.strptime( utc[:26] , '%Y-%m-%d-%H:%M:%S.%f')


    @nodealias("mode")
    def mode_txt(self, mode: int) -> str:
        """ Return a text representation of the mode """
        return get_txt(self.MODE(mode))
    
    @nodealias("qos")    
    def qos_txt(self, qos: int) -> str:
        """ Return a text representation of the qos """
        return get_txt( self.QOS(qos))
        
    @nodealias("status")
    def status_txt(self, status: int) -> str:
        """ Return a text representation of the status """
        return get_txt(self.QOS(status))


if __name__ == "__main__":
    TimeStat( )
