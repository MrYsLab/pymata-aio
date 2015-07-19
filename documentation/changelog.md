#Change Log

###Release 1.2

19 July 2015

Data format returned from i2c_read_request was normalized from Firmata 2byte format to expected data 
representation.



###Release 1.1

18 July 2015

* Fixed bug in data returned from i2c multi-byte read

* Added ability to optionally set "repeated start" for i2c read command
    * Requires the use of FirmataPlus sketch.
    * StandardFirmata Future Release will support this feature, but not currently.

* FirmataPlus updated to be in sync with StandardFirmata 2.4.3

* Updated private_constants.py and constants.py to be consistent with StandardFirmata 2.4.3
    
    
