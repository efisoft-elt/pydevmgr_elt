from pydevmgr_elt.base import EltDevice
from pydevmgr_elt.base.tools import  enum_txt
from valueparser import BaseParser
from systemy import register_factory

from datetime import datetime 
from enum import Enum
Base = EltDevice.Interface

R = Base.Rpc # Base Node
RC = R.Config


class RPC_ERROR(int, Enum):
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

@register_factory("Parser/PlcTime")
class PlcTime(BaseParser, fmt='%Y-%m-%d-%H:%M:%S.%f'):
    @staticmethod
    def __parse__(value, config):
        if isinstance(value, datetime):
            return value.strftime( config.fmt)
        return str(value).replace('T','-')

class TimeRpcs(Base):
    RPC_ERROR = RPC_ERROR

    class Config(Base.Config):
        rpcSetTime: RC = RC(suffix="RPC_SetTime", arg_parsers=[PlcTime])
        rpcSetMode: RC = RC(suffix="RPC_SetMode", arg_parsers=["UaInt32"])

if __name__ == "__main__":
    TimeRpcs()
    print("OK")

