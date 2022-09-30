from ctypes import string_at
from pydantic import BaseModel, root_validator  
from typing import List, Dict
from collections import OrderedDict



class PositionConfig(BaseModel):
    name: str 
    value: float
    
    class Config:
        validate_assignment = True



