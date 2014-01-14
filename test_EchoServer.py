import re
import socket
import time

import BaseTestCase


LISTEN_PORT = 7
TIMEOUT_SECONDS = 30.0
TEST_DATA = 'Test data string.'


class BuildTest(BaseTestCase.BaseTestCase):
	def verifyOutput(self, output):
		# Verify server is listening for connections.
		self.assertRegexpMatches(output, 'Listening for connections...')
		# Parse the CC3000 IP address from the output.
		match = re.search('IP Addr: ([.\d]+)', output)
		self.assertIsNotNone(match)
		ip = match.group(1)
		# Connect to the CC3000 and verify connection is made successfully.
		soc = socket.create_connection((ip, LISTEN_PORT), TIMEOUT_SECONDS)
		self.assertIsNotNone(soc)
		# Send test data.
		soc.sendall(TEST_DATA)
		# Wait a short period for data to be echoed back.
		time.sleep(1.0)
		# Read response and verify it is exactly the same as what was sent.
		response = soc.recv(1024)
		self.assertEqual(response, TEST_DATA)
		# Close the connection.
		soc.shutdown(socket.SHUT_RDWR)
		soc.close()

	def getSketchPath(self):
		return "./EchoServer"
