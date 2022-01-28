from typing import Tuple, Type, Optional

from .config import GROUP
from . import io
from enum import Enum, IntEnum, EnumMeta

class EnumTool:
    """ provide some extention tools for the standard Enum: 
    
    - .txt property. If not set .name is returned  
    - .group property. If not set GROUP.UNKNOWN is returned 
    - if one member of the Enum is called 'UNREGISTERED' it will be sent when Enum(value) refer to a
       unrefered value
       
    Example:
      
    :: 
    
       class COLORS(EnumTool, int, Enum):
           RED = 1
           BLUE = 2
           
           UNREGISTERED = 999
    
          assert COLORS(4).txt == 'UNREGISTERED'
    """
    _txt_ = None
    _group_ = GROUP.UNKNOWN
    
    @property
    def txt(self):
        return self.name if self._txt_ is None else self._txt_        
    
    @txt.setter
    def txt(self, t):
        self._txt_ = t
    
    @txt.deleter
    def txt(self, t):
        del self._txt_
    
    @property
    def group(self):
        return self._group_
    
    
    @group.setter
    def group(self, g):
        self._group_ = g
    
    @group.deleter
    def group(self, t):
        del self._group_
        
    @classmethod
    def _missing_(cls, value):
        try:
            return getattr(cls, 'UNREGISTERED')
        except AttributeError:
            raise ValueError(f'{value} is not a valid {cls.__name__}')
        
def enum_txt(txts: dict ) -> None:
    """ define the enumerator text from a dictionary of IntEnumerator/txt pairs """
    for e, t in txts.items():
        setattr(e, 'txt', t)

def enum_group(groups: dict ) -> None:
    """ define the enumerator gropu from a dictionary of IntEnumerator/GROUP.member pairs """
    for e, g in groups.items():
        setattr(e, 'group', g)

def fjoin(*args) -> str:
    """ join fits elements """
    return " ".join(a.strip() for a in args if a)

def fsplit(key) -> Tuple[str,str]:
    s, _, p = key[::-1].partition(" ")
    return p[::-1], s[::-1]

def _name_attr(cl: Type) -> Type:
    names = {}
    txt = {}
    for subcl in cl.__mro__[::-1]:
        names.update( {n:k for k,n in subcl.__dict__.items() if not k.startswith('_') and isinstance(n, int)} )
        txt.update(getattr(cl, 'txt', {}))
    #cl.names = {n:k for k,n in cl.__dict__.items() if not k.startswith('_')}
    cl.names = names
    cl.txt = {**names, **txt}
    # for c,n in cl.names.items():
    #     setattr( cl, 'is_'+n, classmethod(lambda cl, v, _c_=c: v==_c_))
    return cl

_enum = -1 
def _inc(i: Optional[int] = None) -> int:
    """ number increment to use in frontend 
    
    _inc(0) # reset increment to 0 and return 0 
    _inc()  # increment and return incremented number 
    """
    global _enum
    _enum = _enum+1 if i is None else i
    return _enum

def map2interface_map(map):
    """ Convert an ESO map file to an interface_map as defined in pydevmgr """
    interface_map = {}
    for ikey, imap in map.items():
        if ikey == 'rpc':
            interface_map[ikey] = {
            "type": "Elt",
            "rpc_map": map2rpc_map(imap)
            }
            #tp = "UaRpc"
        else:
            interface_map[ikey] = {
            "type": "Elt",
            "node_map": map2node_map(imap)
            }
            #tp = "UaNode"
        
    return interface_map

def map2node_map(map):
    node_map = {}
    for nkey, suffix in map.items():
        node_map[nkey] = {
            "type": "Elt", 
            "suffix": suffix
        }
    return node_map
    
def map2rpc_map(map):
    rpc_map = {}
    for nkey, suffix in map.items():
        rpc_map[nkey] = {
            "type": "Elt", 
            "suffix": suffix
        }
    return rpc_map

def default_node_map(device_type, interface):
    d = io.load_default_map(device_type)
    d = next(iter(d.values()))        
    if interface == "rpc":
        return map2rpc_map(d[interface])
    else:
        return map2node_map(d[interface])

def default_interface_map(device_type):
    d = io.load_default_map(device_type) 
    d = next(iter(d.values()))  
    return  map2interface_map(d)
    
    
            