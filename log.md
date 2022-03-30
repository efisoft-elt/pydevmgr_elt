0.4.7
=====
- Bug fiex on EltManager when created from devices={}

0.4.6
=====
- Fix the problem of connection deconection in adc, it now shares the same UA connection since 0.4.3 !

0.4.4
=====
- The EnumTool failed in python 3.6 because of a problem when mixing type with Enum. This was fixed in python 3.7.1 
But I prefered to remove EnumTool class. So the Enum are pure 

0.4.3
=====
- remove the __init__ of Adc, handling of prefix is done on the configuration 
- Their is now no need to correct address and namespace because they are ignored since fix in pydevmgr_ua v0.4.2

0.4.2
=====
- the adc address was copied to its motor but not the namespac. Fixed.
- in EltManager and ADC the default kind if set to Device for device children 

0.4.1
=====
Add a default motors config in Adc.Config so it can be built without motors as arguments 


0.4.0
=====
The 0.4.0 is consisders as the version trending to a stable release. Many aspects has been writen from the ground. 

