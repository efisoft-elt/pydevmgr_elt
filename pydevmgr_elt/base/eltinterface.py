from pydevmgr_ua import UaInterface
from pydevmgr_core import record_class, ksplit, get_class

from typing import Dict, Any, Optional
from .tools import fjoin , default_node_map
from .eltnode import EltNode
from .eltrpc import EltRpc
from . import io
from pydantic import root_validator


@record_class
class EltInterface(UaInterface):
    Node = EltNode
    Rpc = EltRpc
    class Config(UaInterface.Config):
        type: str = "Elt"
            
    def __init__(self, *args, fits_key: str = "", **kwargs):
        super().__init__(*args, **kwargs)
        self.fits_key = fits_key
    
    @classmethod
    def new_args(cls, parent, config):
        d = super().new_args(parent, config)
        d.update(fits_key = parent.fits_key)
        return d
    
    @classmethod
    def default_node_map(cls):
        dev, it = ksplit(cls.Config.__fields__['type'].default)
        it = it.lower()
        if it == "rpc": return {}
        try:
            map = default_node_map( dev, it)
        except (ValueError, OSError):
            return {}
        
        #map = {k:EltNode.Config.parse_obj(n) for k,n in map.items()  }
        return map
        
    @classmethod
    def default_rpc_map(cls):
        dev, it = ksplit(cls.Config.__fields__['type'].default)
        it = it.lower()
        if it != "rpc": return {}
        try:
            map = default_node_map( dev, it)
        except (ValueError, OSError):
            return {}        
        #map = {k:EltRpc.Config.parse_obj(r) for k,r in map.items()  }        
        return map    
     
    def get_nodes(self, node_names  = None):
        raise DeprecationWarning('get_nodes is deprecated use the .nodes attribute instead')
    
    @property
    def all_nodes(self) -> list:    
        raise DeprecationWarning('.all_nodes is deprecated use the .nodes attribute instead')
    
    @property
    def all_native_nodes(self) -> list:
        """ deprecated  use the .nodes attribute instead """
        raise DeprecationWarning('.all_native_nodes is deprecated use the .nodes attribute instead')
        
     
