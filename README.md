CC3000 Automated Test Suite
===========================

This tool will automatically run a suite of end-to-end tests to verify the 
Adafruit CC3000 wi-fi chip functionality.  This test suite is useful for 
verifying changes to the CC3000 library.

Created by Tony DiCola (tony@tonydicola.com) for Adafruit

Released under an [MIT license](http://opensource.org/licenses/MIT).

Requirements
------------

You will need the following to use run the tests:

-	[Python 2.7+](http://www.python.org/)
	
	This tool has not yet been tested on Python 3.

-	[Arduino software](http://arduino.cc/)

	Arduino software must be installed somewhere on your computer.

-	[Ino](http://inotool.org/)

	Ino is a command line set of tools to build and upload Arduino sketches.
	This tool is used to automate building and uploading the test sketches in
	this project.  

	NOTE: Ino currently supports only Linux or Mac OSX.  Unfortunately Windows
	is not yet supported, and as a consequence this test suite will not yet run
	on Windows.

	You can easily install Ino using [pip](http://www.pip-installer.org/en/latest/)
	with the command:

		sudo pip install ino

-	[PySerial](http://pyserial.sourceforge.net/)

	PySerial is used to read the serial output of hardware under test.  This library
	can be easily installed using pip with the command:

		sudo pip install pyserial

-	[CC3000 Hardware](http://learn.adafruit.com/adafruit-cc3000-wifi)

	You need to have a basic CC3000 hardware setup with an Arduino (uno, mega,
	or nano) connected to a CC3000, and your computer through a serial/USB port.
	No other hardware should be attached to the Arduino.  See the [CC3000 tutorial](http://learn.adafruit.com/adafruit-cc3000-wifi)
	for an example of how to hook up the CC3000 to an Arduino.

-	A wireless network with internet access that the CC3000 can connect to.

Installation
------------

Once the dependencies above are met, install the test suite by cloning this
repository, or downloading the repository and unpacking to a folder.

Usage
-----

Before running the tests, you must created a 'hardware.cfg' file in the folder
with this test suite.  This is a simple text configuration file which specifies
required and optional information about the hardware under test.

An example and format of this file is as follows (note all section and option
names must be in lower case):

	[hardware]
	# REQUIRED VALUES:
	# Serial port which is connected to the Arduino + CC3000 hardware.
	serial_port = /dev/ttyUSB1
	# Arduino pin which is connected to the CC3000 IRQ pin.
	adafruit_cc3000_irq = 3
	# Arduino pin which is connected to the CC3000 VBEN pin.
	adafruit_cc3000_vbat = 5
	# Arduino pin which is connected to the CC3000 CS pin.
	adafruit_cc3000_cs = 10
	# SSID of the wireless network to use for tests.
	wlan_ssid = your_wireless_network_SSID
	# Password of the wireless network.
	wlan_pass = your_wireless_network_password
	# Type of security for the wireless network.
	# Can be WLAN_SEC_UNSEC, WLAN_SEC_WEP, WLAN_SEC_WPA or WLAN_SEC_WPA2
	wlan_security = WLAN_SEC_WPA2
	# OPTIONAL VALUES:
	# Arduino board model.  Default value is an Arduino Uno.
	# To see a list of possible values, run the 'ino list-models' command.
	board_model = nano328
	# Path to the Arduino software.  If not specified, Ino will try to find the
	# software in its typical install locations.
	arduino_dist = ~/arduino-1.0.5
	# Baud rate to use for serial communication with test sketches.
	# Default value is 115200 baud.
	baud_rate = 115200
	# Time in seconds to wait for a sketch to run before verifying the serial output.
	# Default value is 60 seconds.
	read_timeout_seconds = 60

Once the configuration file is created, tests are run using the Python unittest
runner.  You can run all tests by executing this command from inside the test
suite folder:

	python -m unittest discover

Make sure your hardware is connected to the serial/USB cable, and the configuration
file is set correctly before running!  Once executed, each test will run by 
compiling the appropriate test sketch, uploading to the hardware, waiting a period
of time for serial output, and verifying the serial output.  Success or failure
of tests will be indicated at the completion of the test run.  Individual tests
can be run by [invoking the unittest runner appropriately](http://docs.python.org/2/library/unittest.html#command-line-interface).  Other python test runners should also be compatible with this test
suite, but none have been tested.

Adding Tests
------------

To add a new test, follow these steps:

1.	Create a subdirectory for the test.  For example:

		mkdir newtest

2.	Create a lib and src subdirectory inside the test subdirectory.  This creates
	a sketch that is compatible with the Ino tool.

		cd newtest
		mkdir src
		mkdir lib

3.	Create a symbolic link to the CC3000 library inside the lib subfolder.  Each
	test will reference the same copy of the CC3000 library in this way.

		cd lib
		ln -s ../../Adafruit_CC3000_Library/ Adafruit_CC3000_Library

	If your new test sketch has other library dependencies, place them inside the
	lib folder too (either explicitly or with symbolic links).

4.	Create the sketch .ino file inside the src subdirectory.

	NOTE: Your sketch should use the following defines to configure the CC3000.
	These defines follow the naming and conventions of the CC3000 example sketches:

	-	ADAFRUIT\_CC3000\_IRQ
	-	ADAFRUIT\_CC3000\_VBAT
	-	ADAFRUIT\_CC3000\_CS
	-	WLAN\_SSID
	-	WLAN\_PASS
	-	WLAN\_SECURITY

	Typically the sketch should perform some actions and output success or failure
	messages to the serial port.  See included tests for an example of how to write
	a new test.

5.	Create a new python test to reference and validate sketch output.

	By default files which begin with test\_* will be discovered automatically,
	so you create a file such as test\_newtest.py inside the test suite root folder.

	This file should contain a class which inherits from BaseTestCase and overrides
	at least the following methods:
	
	-	verifyOutput(self, output)

		This function receives the serial output (as a single string) and should
		perform any necessary validation.  BaseTestCase inherits from python's
		unittest.TestCase so all the various [assert functions](http://docs.python.org/2/library/unittest.html#unittest.TestCase.assertEqual)
		are available for the test's usage.
	
	-	getSketchPath(self)

		This function should return a string that specifies the path to the new
		test folder.  For example:

			return './newtest'

That's it!  The test should now run when all tests are executed.  See the included
tests for examples of how to implement a test.
