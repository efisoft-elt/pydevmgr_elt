from PyQt5 import uic
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QGridLayout

import pydevmgr_elt_qt
from pydevmgr_core_qt.layouts import insert_widgets

from pydevmgr_elt_qt import ShutterLine
from pydevmgr_elt import open_elt_manager
from pydevmgr_core import Downloader

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import  QtCore


if __name__=="__main__":
    app = QApplication(sys.argv)
    
    frame = QFrame()
    #layout = QVBoxLayout()
    layout = QGridLayout(objectName='my_layout')
    layout.setObjectName('my_layout')
    frame.setLayout(layout)
    
    downloader = Downloader()
    
    manager = open_elt_manager("tins/tins.yml", key="fcs")
    
    
    frame.show()
    
    
    for d,l in insert_widgets((d for d in manager.devices if d.config.type!="Piezo"), layout, "line"):
        l.connect(downloader, d)
    for d,l in insert_widgets((d for d in manager.devices if d.config.type!="Piezo"), layout, "ctrl", column=1):
        l.connect(downloader, d)
    
    # for d,l in insert_widgets((d for d in manager.devices if d.config.type!="Piezo"), layout, "line"):
    #     l.connect(downloader, d)
    # 
    # for d,l in insert_widgets((d for d in manager.devices if d.config.type=="Motor"), layout, "ctrl"):
    #     l.connect(downloader, d)
        
    # To refresh the gui we need a timer and connect the download method 
    timer = QtCore.QTimer()
    timer.timeout.connect(downloader.download)
    # 10Hz GUI is nice
    timer.start(100)
    
    manager.connect()
    try:
        app.exec_()
    finally:
        manager.disconnect()
