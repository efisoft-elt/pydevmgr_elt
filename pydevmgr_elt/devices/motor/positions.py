from ctypes import string_at
try:
    from pydantic.v1 import BaseModel
except ModuleNotFoundError:
    from pydantic import BaseModel



class PositionConfig(BaseModel):
    name: str 
    value: float
    
    class Config:
        validate_assignment = True



