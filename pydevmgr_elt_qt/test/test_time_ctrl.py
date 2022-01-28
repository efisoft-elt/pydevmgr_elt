from pydevmgr_elt_qt import TimeCtrl
from pydevmgr_elt import Time
from pydevmgr_core import Downloader

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import  QtCore


if __name__=="__main__":
    app = QApplication(sys.argv)
    devLinker = TimeCtrl(show_ignore_check_box=False)
    devLinker.widget.show()
    downloader = Downloader()
    
    #time = Time.from_cfgfile("tins/time1.yml", "time1", key="time1")
    time = Time(address="opc.tcp://192.168.1.11:4840", prefix="MAIN.timer")
    ctrl = devLinker.connect(downloader, time)
    
    # To refresh the gui we need a timer and connect the download method 
    timer = QtCore.QTimer()
    timer.timeout.connect(downloader.download)
    # 10Hz GUI is nice
    timer.start(100)
    
    time.connect()
    try:
        app.exec_()
    finally:
        time.disconnect()