![logo](https://raw.github.com/MrYsLab/pymata-aio/master/documentation/images/logo.png)
======
pymata_aio is a high performance, non-blocking Python client for the Firmata Protocol that supports
the complete StandardFirmata protocol.


##Major features
* __Python 3.4.3 +__ compatible.
* **Implemented using the high efficiency Python [asyncio](https://docs.python.org/3/library/asyncio.html) library.**
* **Choose From 3 Included APIs**
     * **pymata_core** - a pure asyncio method call API.
     * **pymata3** - a pymata_aio plugin implementing a method call API that acts as a proxy for pymata_core. It shields the user from the details of the asyncio library.
     * **pymata_iot** - a pymata_aio plugin API that implements an [Autobahn](http://autobahn.ws/python/) Websocket server, and uses JSON messaging for application communication. 
          * After downloading and invoking **pymata_iot**, [**control your Arduino from a webpage!**](http://mryslab.github.io/pymata-aio/examples/uno_iot_tester.html)
* **Implements 100% of the StandardFirmata Protocol (StandardFirmata 2.43).**
* **Auto-detects Arduino COM ports.**
* **Provides an Integrated Control-C Handler**
* **FirmataPlus (enhanced StandaradFirmata sketch) included with distribution. It adds support for:**
     * **HC-SRO4 Ultrasonic Distance Sensors using a single pin.**
     * **Stepper Motors.**
     * **Piezo Tone Generation.**
     * **2 Pin Rotary Encoder Support.**
* **Ability to automatically capture and time-stamp user specified analog and digital transient input events on a per-pin basis.**
* **All 3 APIs support callback as well as a polled interface.**


__Detailed package information can be found on the [pymata_aio wiki](https://github.com/MrYsLab/pymata-aio/wiki).__