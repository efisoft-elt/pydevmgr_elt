
from pydevmgr_core import  NodeVar
from pydevmgr_elt.base import EltDevice

from enum import Enum
Base = EltDevice.Interface

N = Base.Node # Base Node
NC = N.Config
NV = NodeVar # used in Data 
#                      _              _   
#   ___ ___  _ __  ___| |_ __ _ _ __ | |_ 
#  / __/ _ \| '_ \/ __| __/ _` | '_ \| __|
# | (_| (_) | | | \__ \ || (_| | | | | |_ 
#  \___\___/|_| |_|___/\__\__,_|_| |_|\__|
# 

##### ###########
# SUBSTATE
class TIME_MODE(int, Enum):
    LOCAL                  =   0    
    UTC                    =   1
    
    UNREGISTERED = -9999


#  ____  _        _     ___       _             __                 
# / ___|| |_ __ _| |_  |_ _|_ __ | |_ ___ _ __ / _| __ _  ___ ___  
# \___ \| __/ _` | __|  | || '_ \| __/ _ \ '__| |_ / _` |/ __/ _ \ 
#  ___) | || (_| | |_   | || | | | ||  __/ |  |  _| (_| | (_|  __/ 
# |____/ \__\__,_|\__| |___|_| |_|\__\___|_|  |_|  \__,_|\___\___| 

class CcsSimStat(Base):
    # Add the constants to this class 
    TIME_MODE = TIME_MODE

    class Config(Base.Config):
        # define all the default configuration for each nodes. 
        # e.g. the suffix can be overwriten in construction (from a map file for instance)
        # all configured node will be accessible by the Interface
        
        target_alt : NC = NC(suffix="stat.data.target_observed_altaz[0]")
        target_az : NC = NC(suffix="stat.data.target_observed_altaz[1]")
        current_alt : NC = NC(suffix="stat.data.current_observed_altaz[0]")
        current_az : NC = NC(suffix="stat.data.current_observed_altaz[1]")
        time_lst: NC = NC(suffix="stat.data.time_lst")
        time_tai: NC = NC(suffix="stat.data.time_tai")
        time_utc: NC = NC(suffix="stat.data.time_utc")
        
        north_angle: NC = NC(suffix="stat.data.north_angle")
        pupil_angle: NC = NC(suffix="stat.data.pupil_angle")
        elevation_direction_angle: NC = NC(suffix="stat.data.elevation_direction_angle")
        ra_at_xy: NC = NC(suffix="stat.data.radec_at_altaz_at_requested_xy[0]")
        dec_at_xy: NC = NC(suffix="stat.data.radec_at_altaz_at_requested_xy[1]")
        alt_at_xy: NC = NC(suffix="stat.data.observed_altaz_at_requested_xy[0]")
        az_at_xy: NC = NC(suffix="stat.data.observed_altaz_at_requested_xy[1]")
        parallactic_angle: NC = NC(suffix="stat.data.parallactic_angle")



    # We can add some nodealias to compute some stuff on the fly 
    # If they node to be configured one can set a configuration above 
    
    # Node Alias here     
    # Build the Data object to be use with DataLink, the type and default are added here 
    class Data(Base.Data):
        
        target_alt: NV[float] = 0.0
        target_az: NV[float] = 0.0 
        current_alt: NV[float] = 0.0
        current_az: NV[float] = 0.0    
        time_lst: NV[float] = 0.0
        time_tai: NV[float] = 0.0
        time_utc: NV[float] = 0.0

        north_angle: NV[float] = 0.0
        pupil_angle: NV[float] = 0.0
        elevation_direction_angle: NV[float] = 0.0
        ra_at_xy: NV[float] = 0.0
        dec_at_xy: NV[float] = 0.0
        alt_at_xy: NV[float] = 0.0
        az_at_xy: NV[float] = 0.0
        parallactic_angle: NV[float] = 0.0



if __name__ == "__main__":
    CcsSimStat( )
