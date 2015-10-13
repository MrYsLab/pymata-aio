#Change Log

##Release 2.6

14 October 2015

### New Feature Added
* Added new KeepAlive feature
    * Requires Use of FirmataPlus, FimrataPlusRB or FirmataPlusLBT
    * Enable with a call to keep_alive, passing in a keep alive period.
        * Keep alives may be set between 1 and 10 seconds.
        * Setting the period to 0 seconds disables the keep alive timer.

##Release 2.5

11 October 2015

* Merged latest changes for SparkFun RedBot experiments
* Fixed bug in accepting com_port parameter
* pymata_iot sends reset to Arduino upon exit

##Release 2.4

4 October 2015

* Control C handling removed from pymata_aio internals.
    * Control C handling must be done by appliction
    * Control C handler examples my be viewed [here](https://github.com/MrYsLab/pymata-aio/tree/master/examples/control_C_handlers)

##Release 2.3

3 October 2015

* Repaired bug in control C handling


##Release 2.2

3 October 2015

* Added IP support for WiFly module allowing wireless SparkFun RedBot operations
* FirmataPlus and FirmataPlusRB resets Arduino code and variables module when send_reset is called
* Cleanup of Control-C handling


##Release 2.1

## This is a major release migration from Python 3.4.3 to Python 3.5

28 Aug 2015

* Converted all code to be Python 3.5 compliant.
    * Removed all @asyncio.coroutine decorators and replaced with "async"
    * Replaced all "yield from" to "await"
* Modified FirmataPlusRB.ino systemResetCallback() to set encoder present to false
* API documentation is now Sphinx generated


##Release 1.9
28 Aug 2015

Sparkfun Redbot Support Changes

* Changed encoder pulse detection in FirmataPlusRB from both leading and rising edges to rising edge only.

* Added paramater in pymata3, encoder_config to support hall effect sensors and be in sync with pymata_core.


##Release 1.8
21 Aug 2015

* Bug fix release for pymata3 - changed all calls from pymata3 to pymata_core to loop.run_until_complete
* Duration parameter in play_tone for pymata3 set to a default of None

##Release 1.7
20 Aug 2015

Fixed issue #20 - Tone not properly activated when using pymata3

FirmataPlusRB updated to report encoder readings every 100 ms.

##Release 1.6
19 Aug 2015

* Modifications in anticipation of the upcoming release of our [Sparkfun RedBot]
(https://www.sparkfun.com/products/12649) support library.

    * Modified data format returned for hall effect wheel encoders.

    * Added an additional Arduino sketch, FirmataPlusRB, that will support the redbot sensors and actuators.

##Release 1.5
15 Aug 2015

* Callbacks for both pymata_core and pymata3 can selected to be either asyncio coroutines or direct calls.
    * Default is direct call.
    
* Option provided in encoder_config() for support of hall effect wheel encoders.

* Minor bug fixes.

* Code cleanup.

##Release 1.4
1 Aug 2015

* Auto Detection for OS X ports repaired from release 1.3. Tested and functioning now.


##Release 1.3
23 July 2015

* Auto detection of OS X serial ports added

* Added a logging feature to optionally redirect console output to a log file.

* Removed SIGALRM from Control-C handler to support Windows.


##Release 1.2

19 July 2015

Data format returned from i2c_read_request was normalized from Firmata 2byte format to expected data 
representation.



##Release 1.1

18 July 2015

* Fixed bug in data returned from i2c multi-byte read

* Added ability to optionally set "repeated start" for i2c read command
    * Requires the use of FirmataPlus sketch.
    * StandardFirmata Future Release will support this feature, but not currently.

* FirmataPlus updated to be in sync with StandardFirmata 2.4.3

* Updated private_constants.py and constants.py to be consistent with StandardFirmata 2.4.3
    
    
