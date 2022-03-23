
from PyQt5 import uic
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QGridLayout

import pydevmgr_elt_qt
from pydevmgr_core_qt.layouts import Layout

from pydevmgr_core_qt.base_view import MultiViewLinker

from pydevmgr_elt_qt import ShutterLine
from pydevmgr_elt import open_elt_manager
from pydevmgr_core import Downloader

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import  QtCore
import yaml 



layout_conf = """
ctrl: # all devices in more complete control widget 
    size: [800,500]
    setup:
        - device: "*"
          layout: ly_devices
          widget_kind: "ctrl"

line: # all devices in one line control widget 
    setup:
        - device: "*"
          layout: ly_devices
          widget_kind: "line"

cfg: # un config panel for Motor devices 
    setup:
        - device: "*"
          dev_type: Motor
          layout: ly_devices
          widget_kind: "cfg"  

motor1: # Focus on motor1 as an exemple 
    size: [1200,500]
    setup:
        - device: motor1              
          widget_kind: "ctrl"
        - device: motor1              
          widget_kind: "cfg"

main: # use an other ui file, left panel general devices, right dedicated tabs 
    ui_file: tins/tins_tab.ui
    setup:
        - device: motor1 
          layout: ly_motor1             
          widget_kind: "ctrl"
        - device: motor1 
          layout: ly_motor1  
          widget_kind: "cfg"
        - device: motor2 
          layout: ly_motor2             
          widget_kind: "ctrl"
        - device: motor2 
          layout: ly_motor2  
          widget_kind: "cfg"
        - device: adc1 
          layout: ly_adc1  
          widget_kind: "ctrl"
        - device: drot1 
          layout: ly_drot1  
          widget_kind: "ctrl"
        - device: shutter1
          layout: ly_devices  
          widget_kind: "ctrl"
        - device: lamp1
          layout: ly_devices  
          widget_kind: "ctrl"
"""
layout_conf = yaml.load(layout_conf)



if __name__=="__main__":
    print(layout_conf)
    app = QApplication(sys.argv)

    mvl = MultiViewLinker(views=layout_conf)
    data = mvl.new_data(current_view="main")
    
    

          
    manager = open_elt_manager("tins/tins.yml", key="fcs")
    downloader = Downloader()
    
    ctrl = mvl.connect( downloader, 
                        list(d for d in manager.devices if d.config.type!="Piezo" ),
                        data
                    )
    
        
    timer = QtCore.QTimer()
    timer.timeout.connect(downloader.download)
    # 10Hz GUI is nice
    timer.start(100)
    
 

    mvl.widget.show()
    manager.connect()
    try:
        app.exec_()
    finally:
        manager.disconnect()  
    
    
    # frame = QFrame()
    # #layout = QVBoxLayout()
    # layout = QGridLayout()
    # frame.setLayout(layout)
    
    # downloader = Downloader()
    
    # manager = open_elt_manager("tins/tins.yml", key="fcs")
    
    
    # frame.show()
    
    
    # for d,l in insert_widgets((d for d in manager.devices if d.config.type!="Piezo"), layout, "line"):
    #     l.connect(downloader, d)
    # for d,l in insert_widgets((d for d in manager.devices if d.config.type!="Piezo"), layout, "ctrl", column=1):
    #     l.connect(downloader, d)
    
    # # for d,l in insert_widgets((d for d in manager.devices if d.config.type!="Piezo"), layout, "line"):
    # #     l.connect(downloader, d)
    # # 
    # # for d,l in insert_widgets((d for d in manager.devices if d.config.type=="Motor"), layout, "ctrl"):
    # #     l.connect(downloader, d)
        
    # # To refresh the gui we need a timer and connect the download method 
    # timer = QtCore.QTimer()
    # timer.timeout.connect(downloader.download)
    # # 10Hz GUI is nice
    # timer.start(100)
    
    # manager.connect()
    # try:
    #     app.exec_()
    # finally:
    #     manager.disconnect()
