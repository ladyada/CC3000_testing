# Adafruit CC3000 Library Test Listener
# Created by Tony DiCola (tony@tonydicola.com)
# Released with the same license as the Adafruit CC3000 library (BSD)

# Create a simple server to listen on a port and save all data received.

from socket import *
import sys
import threading


class TCPListener(object):
	def __init__(self, port):
		# Create listening socket
		self.listen_soc = socket(AF_INET, SOCK_STREAM)
		# Ignore waiting for the socket to close if it's already open.  See the python socket
		# doc for more info (very bottom of http://docs.python.org/2/library/socket.html).
		self.listen_soc.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		# Listen on any network interface for the specified port
		self.listen_soc.bind(('', port))
		self.listen_soc.listen(5)
		# Store recieved data.
		self.received = ''
		# Spawn listening thread.
		self.run = True
		self.listen_thread = threading.Thread(target=self._listen_thread)
		self.listen_thread.daemon = True
		self.listen_thread.start()

	def stop(self):
		self.run = False

	def _listen_thread(self):
		try:
			# Wait for connections and spawn worker threads to process them.
			while self.run:
				client, address = self.listen_soc.accept()
				thread = threading.Thread(target=self._process_connection, args=(client,))
				thread.daemon = True
				thread.start()
		finally:
			self.listen_soc.close()

	def _process_connection(self, client):
		try:
			while self.run:
				data = client.recv(1024)
				if not data: 
					break
				else:
					# Save all received data.
					# TODO: Consider using a lock to stop race conditions with multiple
					# concurrent writes.  The GIL should make this thread safe for now.
					self.received += data
		finally:
			client.close()
