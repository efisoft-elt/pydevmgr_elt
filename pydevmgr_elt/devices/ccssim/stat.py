
from collections import namedtuple
import math
from typing import Type
from pydevmgr_core import  NodeVar, VType
from pydevmgr_core.base.dataclass import set_data_model
from pydevmgr_core.base.node_alias import NodeAlias, NodeAlias1
from pydevmgr_core.nodes import  Rad2Degree
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

_r2d = 180/math.pi
_d2r = math.pi/180.
class Rad2DegreeVect(NodeAlias1):
        def fget(self, angles):
            return angles.__class__( *(a*_r2d for a in angles))
        
        def fset(self, angles_deg):
            return angles_deg.__class__( *(a*_d2r for a in angles_deg))

#  ____  _        _     ___       _             __                 
# / ___|| |_ __ _| |_  |_ _|_ __ | |_ ___ _ __ / _| __ _  ___ ___  
# \___ \| __/ _` | __|  | || '_ \| __/ _ \ '__| |_ / _` |/ __/ _ \ 
#  ___) | || (_| | |_   | || | | | ||  __/ |  |  _| (_| | (_|  __/ 
# |____/ \__\__,_|\__| |___|_| |_|\__\___|_|  |_|  \__,_|\___\___| 


RaDec = namedtuple("RaDec", ["ra", "dec"])
AltAz = namedtuple("AltAz", ["alt", "az"])
RaDecType = (RaDec, RaDec(0.0, 0.0))
AltAzType = (AltAz, AltAz(0.0, 0.0))

class AltAzNode(Base.Node):
    class Config:
        vtype: VType  = (AltAz, AltAz(0.0, 0.0))
    def parse_output(self, value):
        return AltAz(*value)

class RaDecNode(Base.Node):
    class Config:
        vtype: VType = (RaDec, RaDec(0.0, 0.0))
    def parse_output(self, value):
        return RaDec(*value)

@set_data_model
class CcsSimStat(Base):
    # Add the constants to this class 
    TIME_MODE = TIME_MODE

    class Config(Base.Config):
        # define all the default configuration for each nodes. 
        # e.g. the suffix can be overwriten in construction (from a map file for instance)
        # all configured node will be accessible by the Interface
        
        pass
        target_altaz =  AltAzNode.Config(suffix="stat.data.target_observed_altaz")
        current_altaz = AltAzNode.Config(suffix="stat.data.current_observed_altaz")
        time_lst: NC = NC(suffix="stat.data.time_lst", vtype=float)
        time_tai: NC = NC(suffix="stat.data.time_tai", vtype=float)
        time_utc: NC = NC(suffix="stat.data.time_utc", vtype=float)
        
        north_angle: NC = NC(suffix="stat.data.north_angle", vtype=float)
        pupil_angle: NC = NC(suffix="stat.data.pupil_angle", vtype=float)
        elevation_direction_angle: NC = NC(suffix="stat.data.elevation_direction_angle", vtype=float)
        radec_at_xy = RaDecNode.Config(suffix="stat.data.radec_at_altaz_at_requested_xy")
        altaz_at_xy = AltAzNode.Config(suffix="stat.data.observed_altaz_at_requested_xy")
        parallactic_angle: NC = NC(suffix="stat.data.parallactic_angle", vtype=float)

        

    target_altaz_deg = Rad2DegreeVect.Config( node="target_altaz", vtype=AltAzType)
    current_altaz_deg = Rad2DegreeVect.Config( node="current_altaz", vtype=AltAzType)
    north_angle_deg = Rad2Degree.Config( node="north_angle", vtype=float)
    pupil_angle_deg = Rad2Degree.Config( node="pupil_angle", vtype=float)
    elevation_direction_angle_deg = Rad2Degree.Config( node="elevation_direction_angle", vtype=float)
    parallactic_angle_deg = Rad2Degree.Config( node="parallactic_angle", vtype=float)



if __name__ == "__main__":
    CcsSimStat( )
