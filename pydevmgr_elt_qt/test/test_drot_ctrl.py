from pydevmgr_elt_qt import DrotCtrl
from pydevmgr_elt import open_device
from pydevmgr_core import Downloader

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import  QtCore


if __name__=="__main__":
    app = QApplication(sys.argv)
    devLinker = DrotCtrl()
    devLinker.widget.show()
    downloader = Downloader()
    
    device = open_device("tins/drot1.yml", key="drot1")
    
    ctrl = devLinker.connect(downloader, device)
    
    # To refresh the gui we need a timer and connect the download method 
    timer = QtCore.QTimer()
    timer.timeout.connect(downloader.download)
    # 10Hz GUI is nice
    timer.start(100)
    
    device.connect()
    try:
        app.exec_()
    finally:
        device.disconnect()