import os
import serial
import subprocess
import time
import unittest

from Configuration import config


class BaseTestCase(unittest.TestCase):
	"""
	Base class for building CC3000 tests.  Test implementors must inherit from
	this class and provide an implemenetation of verifyOutput and getSketchPath.
	This class inherits from the unittest.TestCase class and provides all of its
	inherited functionality like assertion, setUp, and tearDown functions.
	"""

	def verifyOutput(self, output):
		"""
		Override this function to provide verification of the serial output 
		produced after the test sketch is loaded on the hardware.
		Output parameter is a text string with the serial output.
		"""
		raise NotImplementedError

	def getSketchPath(self):
		"""
		Override this function to return a string path to the test sketch
		folder.
		"""
		raise NotImplementedError

	def getReadTimeout(self):
		"""
		Optionally override this function to return the number of seconds to
		wait for serial output to be collected after the test sketch is loaded
		on the hardware.
		By default this function returns the read timeout value defined in the
		configuration file.
		"""
		return config.read_timeout_seconds

	def getSketchParameters(self):
		"""
		Return a dictionary of custom #DEFINE parameters that are passed to the sketch.
		Each dictionary entry should have a string key that is the define name, and a
		string value that is the define value.  For example a sketch that has:
		  int foo = BAR;
		Can have the parameter BAR set to the value 10 by returning the following
		dictionary from this function:
		  { 'BAR': 10 }
		"""
		return {}

	def runTest(self):
		# Build the test sketch.
		options = ''
		if config.board_model is not None:
			options += ' --board-model %s' % config.board_model
		if config.arduino_dist is not None:
			options += ' --arduino-dist %s' % config.arduino_dist
		command = 'ino build'
		command += options
		command += (' --cppflags="'
					' -DADAFRUIT_CC3000_IRQ=%s'
					' -DADAFRUIT_CC3000_VBAT=%s'
					' -DADAFRUIT_CC3000_CS=%s'
					# This completely unreadable incantation of single quotes, 
					# double quotes, and backslashes is necessary to quote the 
					# string parameters passed to the compiler through multiple 
					# levels of shell interpretation.  The intended output is a
					# flag like -DWLAN_SSID=\"foo\" where foo is the SSID.
					' \'-DWLAN_SSID=\\\\"\'"\'"%s\\\\"\'"\'"\''
					' \'-DWLAN_PASS=\\\\"\'"\'"%s\\\\"\'"\'"\''
					' -DWLAN_SECURITY=%s' % 
						(config.adafruit_cc3000_irq,
							 config.adafruit_cc3000_vbat,
							 config.adafruit_cc3000_cs,
							 config.wlan_ssid,
							 config.wlan_pass,
							 config.wlan_security))
		for key, value in self.getSketchParameters().iteritems():
			command += ' -D%s=%s' % (key, value)
		command += ' -ffunction-sections -fdata-sections -g -Os -w"'
		subprocess.check_call(command, shell=True, cwd=self.getSketchPath())
		# Upload the test sketch.
		command = 'ino upload'
		command += options
		command += ' --serial-port %s' % config.serial_port
		subprocess.check_call(command, shell=True, cwd=self.getSketchPath())
		# Verify the serial output.
		timeout = self.getReadTimeout()
		print 'Waiting', timeout, 'seconds to capture serial output...'
		with serial.Serial(config.serial_port, 
						   config.baud_rate, 
						   timeout=timeout) as ser:
			start = time.time()
			output = ''
			while time.time() - start < timeout:
				output += ser.readline()
			self.verifyOutput(output)
