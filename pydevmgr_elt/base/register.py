from pydevmgr_core import register as _register

def register(*args, namespace="elt", **kwargs):
    """ class register wit default namespace 'elt' """
    return _register(*args, namespace=namespace, **kwargs) 
