from opcua.client.client import Client
from pydevmgr_core.base.datamodel import DataLink
from pydevmgr_core.base.download import DataView
from pydevmgr_elt import CcsSim 
from pydevmgr_core import download, BaseNode 


if False:
    def test_ccs_cfg_live():
        with CcsSim(prefix="MAIN.ccs_sim", address="opc.tcp://192.168.1.11:4840") as ccs:
            print(download( ccs.cfg.find( BaseNode, -1)))

    def test_ccs_stat_live():
        with CcsSim(prefix="MAIN.ccs_sim", address="opc.tcp://192.168.1.11:4840") as ccs:
            data = CcsSim.Stat.Data()  
            DataLink(ccs.stat, data ).download()
            print(data)


    def test_ccs_ctrl_live():
        with CcsSim(prefix="MAIN.ccs_sim", address="opc.tcp://192.168.1.11:4840") as ccs:
            data = CcsSim.Ctrl.Data()  
            DataLink(ccs.ctrl, data ).download()
            print(data)

    test_ccs_cfg_live()
