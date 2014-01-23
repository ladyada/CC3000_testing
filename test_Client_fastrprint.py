import re
import socket
import time

import BaseTestCase
import Listener


SERVER_PORT = 9000


class Client_fastrprint(BaseTestCase.BaseTestCase):
	def getLocalIP(self):
		# Ugly hack to get the local IP, see: http://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
		# Unfortunately calling socket.gethostbyname(socket.gethostname()) returns 127.0.0.1
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("adafruit.com",80))
		localip = s.getsockname()[0]
		s.close()
		return localip

	def getSketchParameters(self):
		# Send the IP and port for the test server.
		a, b, c, d = self.getLocalIP().split('.')
		return { 'SERVER_PORT': SERVER_PORT,
				 'SERVER_IP_A': a, 
				 'SERVER_IP_B': b,
				 'SERVER_IP_C': c,
				 'SERVER_IP_D': d }

	def setUp(self):
		# Start a server to listen for output from the server.
		self.server = Listener.TCPListener(SERVER_PORT)

	def verifyOutput(self, output):
		# Verify tests are done running and no failures occured.
		self.assertRegexpMatches(output, 'Tests finished!')
		self.assertNotRegexpMatches(output, 'FAILURE:')
		# Stop server and verify received data.
		self.server.stop()
		expected = 'Fastrprint string.Fastrprint with a large (>32 character) character string!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Fastrprintln string.\n\rFastrprintln with a large (>32 character) character string!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\rFastrprint flash.Fastrprint with a large (>32 character) flash string!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Fastrprintln flash.\n\rFastrprintln with a large (>32 character) flash string!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\r\n\r\n\rThis is a message for client 1.This is a message for client 2.This is a flash message for client 1.This is a flash message for client 2.This is a large (>32 character) flash message for client 1!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!This is a large (>32 character) flash message for client 2!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
		self.assertEqual(self.server.received, expected)

	def getSketchPath(self):
		return "./Client_fastrprint"
