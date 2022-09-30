from pydantic import BaseModel, validator
from typing import List
from enum import Enum 
from dataclasses import dataclass



##### ############
# Sequence
class InitSeqNumber(int, Enum):
    END = 0
    FIND_INDEX = 1
    FIND_REF_LE = 2
    FIND_REF_UE = 3
    FIND_LHW = 4
    FIND_UHW = 5

    DELAY = 6
    MOVE_ABS = 7
    MOVE_REL = 8
    CALIB_ABS = 9
    CALIB_REL = 10
    CALIB_SWITCH = 11

@dataclass
class InitSeqDefinition:
    number: InitSeqNumber = InitSeqNumber.END
    var1: str = "" 
    var2: str = ""
    
init_sequence_loockup = {
       'END': InitSeqDefinition( InitSeqNumber.END,  "", "" ),
        'FIND_ENDEX': InitSeqDefinition( InitSeqNumber.FIND_INDEX, "Fast Vel", "Slow Vel" ),
        'FIND_REF_LE': InitSeqDefinition( InitSeqNumber.FIND_REF_LE, "Fast Vel", "Slow Vel" ),
        'FIND_REF_UE': InitSeqDefinition( InitSeqNumber.FIND_REF_UE, "Fast Vel", "Slow Vel" ),
        'FIND_LHW': InitSeqDefinition( InitSeqNumber.FIND_LHW, "Fast Vel", "Slow Vel" ),
        'FIND_UHW': InitSeqDefinition( InitSeqNumber.FIND_UHW, "Fast Vel", "Slow Vel" ),
        'DELAY': InitSeqDefinition( InitSeqNumber.DELAY, "Delay [ms]", "" ),
        'MOVE_ABS': InitSeqDefinition( InitSeqNumber.MOVE_ABS, "Vel", "Pos" ),
        'MOVE_REL': InitSeqDefinition( InitSeqNumber.MOVE_REL, "Vel", "Pos" ),
        'CALIB_ABS': InitSeqDefinition( InitSeqNumber.CALIB_ABS, "Pos", "" ),
        'CALIB_REL':InitSeqDefinition( InitSeqNumber.CALIB_REL, "Pos", "" ),
        'CALIB_SWITCH':InitSeqDefinition( InitSeqNumber.CALIB_SWITCH, "Pos", "" ),
}    



# ################################        
    
class InitSeqequenceStep(BaseModel):
    """ Data  Model for step configuration """
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    step: str =  "END"    
    value1: float = 0.0
    value2: float = 0.0
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~

    @validator('step')
    def _validate_step(cls, step):
        try:
            init_sequence_loockup[step]
        except KeyError:
            raise ValueError()
        return step  
    class Config:                
        validate_assignment = True
# ################################




class InitialisationConfig(BaseModel):
    __root__ : List[InitSeqequenceStep] = []
    



# class InitialisationConfigV3(BaseModel):
#     """ Config Model for the initialisation sequence """
#     # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     # Data Structure 
#     # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     sequence : List[str] = []
#     END          : SeqStepConfig = SeqStepConfig(index=0) 
#     FIND_INDEX   : SeqStepConfig = SeqStepConfig(index=1)
#     FIND_REF_LE  : SeqStepConfig = SeqStepConfig(index=2)
#     FIND_REF_UE  : SeqStepConfig = SeqStepConfig(index=3)
#     FIND_LHW     : SeqStepConfig = SeqStepConfig(index=4)
#     FIND_UHW     : SeqStepConfig = SeqStepConfig(index=5)  
#     DELAY        : SeqStepConfig = SeqStepConfig(index=6)
#     MOVE_ABS     : SeqStepConfig = SeqStepConfig(index=7)
#     MOVE_REL     : SeqStepConfig = SeqStepConfig(index=8)
#     CALIB_ABS    : SeqStepConfig = SeqStepConfig(index=9)
#     CALIB_REL    : SeqStepConfig = SeqStepConfig(index=10)
#     CALIB_SWITCH : SeqStepConfig = SeqStepConfig(index=11)
#     # ~~~~~~~~~~~~~~~~~~~~~~~~~~
#     class Config:                
#         validate_assignment = True        
#     # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     # Data Validator Functions
#     # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     @validator('END', 'FIND_INDEX', 'FIND_REF_LE', 'FIND_REF_UE', 'FIND_LHW', 'FIND_UHW', 
#                'DELAY', 'MOVE_ABS', 'MOVE_REL', 'CALIB_ABS', 'CALIB_REL' , 'CALIB_SWITCH')
#     def force_index(cls, v, field):
#         """ need to write the index """        
#         v.index = getattr(InitSeqNumber, field.name)
#         return v

#     @validator('sequence')
#     def validate_initialisation(cls,sequence):   
#         """ Validate the list of sequence """ 
#         for s in sequence:
#             try:
#                 cls.__fields__[s]
#             except KeyError:
#                 raise ValueError(f'unknown sequence step named {s!r}')
#         return sequence
#     # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     # Method to save back the configuration     
#     def cfgdict(self):
#         d = {'sequence':self.sequence}
#         for seq in self.sequence:
#             d[seq] = getattr(self, seq).cfgdict()            
#         return d
# ################################



def init_sequence_to_cfg(initialisation, loockup=init_sequence_loockup):
    """ from a config initialisation dict return a dictionary of key/value for .cfg interface """            
    if not initialisation:
        return {}
    
    # set the init sequence    
    cfg_dict = {}
    for i in range(1, 11):
        cfg_dict["init_seq{}_action".format(i)] = int(InitSeqNumber.END)
        cfg_dict["init_seq{}_value1".format(i)] = 0.0
        cfg_dict["init_seq{}_value2".format(i)] = 0.0


    for i,step in enumerate(initialisation, start=1):
        definition = loockup[step.step]
        cfg_dict["init_seq{}_action".format(i)] = int(definition.number)
        cfg_dict["init_seq{}_value1".format(i)] = step.value1 
        cfg_dict["init_seq{}_value2".format(i)] = step.value2
    
    return cfg_dict

