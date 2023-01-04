from pydevmgr_ua import UaNode
from .eltengine import EltNodeEngine
from .register import register 

class EltNodeConfig(UaNode.Config, EltNodeEngine.Config):
        type: str = "Elt"


@register
class EltNode(UaNode):
    Config = EltNodeConfig
    Engine = EltNodeEngine
    

