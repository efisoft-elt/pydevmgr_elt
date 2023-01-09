from pydevmgr_elt import Drot, BaseNode, download
from pydevmgr_elt import CcsSim 

url = "opct.tcp://192.168.1.11:4840"

if __name__ == "__main__":

    with Drot( address=url,  prefix="MAIN.drot1")  as drot:

        l = list( drot.find( BaseNode, -1))
        print(l) 
        print( download(l) )
    
    with CcsSim( address=url, prefix="MAIN.ccs_sim") as ccs:
        l = list( ccs.find( BaseNode, -1))[4:6]
        print( *(n.config.suffix for n in l)) 

        print( download( l) )
