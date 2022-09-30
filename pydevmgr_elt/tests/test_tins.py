
from pydevmgr_elt import BaseNode, open_elt_manager, download, DataLink , wait
from pydevmgr_elt import eltconfig

eltconfig.host_mapping = {"opc.tcp://myplc.local:4840":"opc.tcp://192.168.1.11:4840"}
m = open_elt_manager( "tins/tins.yml" )

# data_dict = {}

# data = m.create_data_class(  m.children(m.Device)   )()
# dl = DataLink(m, data)

# if __name__ == "__main__":

#     try:    
#         m.connect()

#         download( m.find(BaseNode, -1), data_dict )
#         dl.download()   
        
#         m.configure()
        
#         print( "Resetting ...", end="" )
#         wait(m.reset()) 
#         print( "OK" )

#         print( "Initialising ...", end="" )
#         wait(m.init()) 
#         print( "OK" )
        
#         print( "Enabling ...", end="" )
#         wait(m.enable()) 
#         print( "OK" )
        


    

        
#     finally:
#         m.disconnect()
