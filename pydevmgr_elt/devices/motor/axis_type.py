from enum import Enum 
from valueparser import BaseParser
from systemy import register_factory

from pydevmgr_ua import UaInt32

class AXIS_TYPE(int, Enum):
    LINEAR = 1
    CIRCULAR =2
    CIRCULAR_OPTIMISED = 3

to_int32 = UaInt32().parse 

def axis_type(axis_type):
    """ return always a axis_type int number from a number or a string
    
    Raise a ValueError if the input string does not match axis type
    Example:
        axis_type('LINEAR') == 1
        axis_type(1) == 1
    """
    if isinstance(axis_type, str):
        try:
            axis_type = getattr(AXIS_TYPE, axis_type) 
        except AttributeError:
            raise ValueError(f'Unknown AXIS type {axis_type!r}')
    return to_int32(axis_type)

# a parser class for axis type
@register_factory("Parser/AxisType")
class AxisType(BaseParser):
    @staticmethod
    def __parse__(value, config):
        return axis_type(value)   


