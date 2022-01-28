#! /usr/bin/env python
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys, os
from pydevmgr_elt import Downloader, open_manager
from pydevmgr_qt.manager import ManagerMain
from pydevmgr_qt import io
from pydevmgr_core import io as pio

usage = "pydevmgr_gui relative/path/to/manager.yml"

# if len(sys.argv)!=2:
#     print(usage)
#     sys.exit(1)

mgr = None
def app_main():
    global mgr
    
    option = {}
    if len(sys.argv)<3: 
        file_body, _ = os.path.splitext(sys.argv[1])
        
        try:
            option['ui_resource'] = io.find_ui(file_body+".ui")
        except (IOError, ValueError):
            pass
    else:
        try:
            option['ui_resource'] = io.find_ui(sys.argv[2])
        except (IOError, ValueError):
            print(usage)
            print("\nCannot find ui file {}".format(sys.argv[2]))
            raise ValueError()
        
            
        
        
        
    mgr = open_manager(sys.argv[1], '')
    
    mgr.connect()
    #mgr.configure() # configure through OPC-UA all the devices !!!!!!!
    
    downloader = Downloader()
    

    app = QApplication(sys.argv)
    
    linker = ManagerMain()
    linker.connect(downloader, mgr, link_failure=True)
        
    linker.widget.show()
    
    timer = QtCore.QTimer()
    timer.timeout.connect(downloader.download)
    
    timer.start(200)
    return app.exec_()

def main():
    global mgr
    exit_code = 1
    if len(sys.argv)<2:
        print(usage)
        print("\nManager file found in $CFGPATH:")
        for f,r in pio.explore_config("Manager"):
            print(f"    {f}    inside {r}")
        return 1
    
    try:
        exit_code = app_main()
    except Exception as e:
        if mgr:        
            mgr.disconnect()
        raise e
    else:
        mgr.disconnect()
        sys.exit(exit_code)

if __name__ == '__main__':
    main()

    # exit_code = 1
    # try:
    #     exit_code = main()
    # except Exception as e:
    #     if mgr:        
    #         mgr.disconnect_all()
    #     raise e
    # else:
    #     mgr.disconnect_all()
    #     sys.exit(exit_code)
    # finally:
    #     if mgr:        
    #         mgr.disconnect_all()
    #         sys.exit(exit_code)
    # 