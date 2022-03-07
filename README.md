
This python package is used to handle ELT standard devices directly from python objects and through OPC-UA. 

The package is intended to be used when a full instrument ELT software is not available but scripting needs to be done on devices and using the Low Level ELT software (Running on Beckhoff PLC). 
A good exemple of the use case is making sequences of initialisation and movement of motors for AIT purposes without the
need to buil a high level ELT software. 

The documentation (for version >=0.3) is [here](https://pydevmgr-elt.readthedocs.io/en/latest/pydevmgr_elt_manual.html)     

Sources are [here](https://github.com/efisoft-elt/pydevmgr_elt)


# Install

```bash
> pip install pydevmgr_elt 
```

From sources :

```bash
> git clone https://github.com/efisoft-elt/pydevmgr_elt
> cd pydevmgr_elt 
> python setup.py install
```


# Basic Usage


```python 
from pydevmgr_elt import Motor, wait
m1 = Motor('motor1', address="opc.tcp://192.168.1.11:4840", prefix="MAIN.Motor1")

try:
    m1.connect()    
    wait(m1.move_abs(7.0,1.0), lag=0.1)
    print( "position is", m1.stat.pos_actual.get() )
finally:
    m1.disconnect()
```

```python 
from pydevmgr_elt import Motor, DataLink

m1 = Motor('motor1', address="opc.tcp://152.77.134.95:4840", prefix="MAIN.Motor1")

m1_data = Motor.Data() # m1_data is a structure built with default value
m1_dl = DataLink(m1, m1_data) # create a data link use to fill m1_data to real hw values

try:
    m1.connect()
    m1_dl.download()
    
    print( m1_data.stat.pos_actual,   m1_data.stat.pos_error  )
finally:
    m1.disconnect()

```

Open from an elt yaml configuration file as defined in ELT IFW v3

```python
from pydevmgr_elt import open_elt_device
motor1 = open_elt_device( "tins/motor1.yml" )
```
