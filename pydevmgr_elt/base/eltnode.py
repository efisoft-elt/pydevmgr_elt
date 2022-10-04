from pydevmgr_ua import UaNode
from pydevmgr_core import kjoin, record_class
from .eltengine import EltNodeEngine


class EltNodeConfig(UaNode.Config, EltNodeEngine.Config):
        type: str = "Elt"


@record_class
class EltNode(UaNode):
    Config = EltNodeConfig
    Engine = EltNodeEngine
    

