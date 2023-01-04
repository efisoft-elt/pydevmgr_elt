from pydevmgr_ua import UaInterface
from .register import register 
from .eltnode import EltNode
from .eltrpc import EltRpc
from .eltengine import EltEngine 


@register
class EltInterface(UaInterface):
    Engine = EltEngine
    
    Node = EltNode
    Rpc = EltRpc
    class Config(UaInterface.Config, extra="allow"):
        Node = EltNode.Config
        Rpc = EltRpc.Config
        type: str = "Elt"
                
