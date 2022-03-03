
from pydevmgr_elt_qt import MotorPlot
from pydevmgr_elt import Motor
from pydevmgr_core import Downloader

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import  QtCore


if __name__=="__main__":
    app = QApplication(sys.argv)
    devLinker = MotorPlot(show_ignore_check_box=False, link_failure=False)
    devLinker.widget.show()
    downloader = Downloader()
    
    motor = Motor.from_cfgfile("tins/motor1.yml", path="motor1", key="motor1")
    
    ctrl = devLinker.connect(downloader, motor)
    
    # To refresh the gui we need a timer and connect the download method 
    timer = QtCore.QTimer()
    timer.timeout.connect(downloader.download)
    # 10Hz GUI is nice
    timer.start(100)
    
    motor.connect()
    try:
        app.exec_()
    finally:
        motor.disconnect()
