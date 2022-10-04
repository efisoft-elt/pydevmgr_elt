from pydevmgr_ua import UaInterface
from pydevmgr_core import record_class, ksplit, get_class

from typing import Dict, Any, Optional
from .tools import fjoin 
from .eltnode import EltNode
from .eltrpc import EltRpc
from .eltengine import EltEngine 
from . import io
from pydantic import root_validator


@record_class
class EltInterface(UaInterface):
    Engine = EltEngine
    
    Node = EltNode
    Rpc = EltRpc
    class Config(UaInterface.Config, extra="allow"):
        Node = EltNode.Config
        Rpc = EltRpc.Config
        type: str = "Elt"
                
