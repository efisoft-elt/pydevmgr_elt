from pydevmgr_elt_qt import MotorLine
from pydevmgr_elt import Motor
from pydevmgr_core import Downloader

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import  QtCore

_online = True

if __name__=="__main__":
    app = QApplication(sys.argv)
    devLinker = MotorLine()
    devLinker.widget.show()
    downloader = Downloader()
    
    motor = Motor.from_cfgfile("tins/motor1.yml", "motor1")
    
    ctrl = devLinker.connect(downloader, motor)
    
    # To refresh the gui we need a timer and connect the download method 
    timer = QtCore.QTimer()
    timer.timeout.connect(downloader.download)

    if _online:
        # 10Hz GUI is nice
        timer.start(100)
        
        motor.connect()
    try:
        app.exec_()
    finally:
        motor.disconnect()
