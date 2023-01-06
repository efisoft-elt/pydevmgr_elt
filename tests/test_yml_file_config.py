import pytest 
from pydevmgr_elt import EltDevice


def test_dev_endpoint_behavior():

    adr = "opc.tcp://143.123.45:8888"
    c = EltDevice.Config( dev_endpoint=adr)
    assert c.dev_endpoint == c.address
    c2 = EltDevice.Config( address=adr)
    assert c2.address == c.address






if __name__ == "__main__":
   test_dev_endpoint_behavior() 

