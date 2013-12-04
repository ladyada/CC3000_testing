import ConfigParser


SECTION = 'hardware'
CONFIG_FILENAME = 'hardware.cfg'


class Configuration(object):
	def __init__(self):
		# Load the configuration file.
		config = ConfigParser.SafeConfigParser()
		try:
			with open(CONFIG_FILENAME, 'r') as cfgfile:
				config.readfp(cfgfile)
		except IOError:
			raise IOError('Could not find configuration file %s!  See README.md'
						  ' for the format and an example.' % CONFIG_FILENAME)
		# Parse required parameters.
		self.serial_port = config.get(SECTION, 'serial_port')
		self.adafruit_cc3000_irq = config.getint(SECTION, 'adafruit_cc3000_irq')
		self.adafruit_cc3000_vbat = config.getint(SECTION, 'adafruit_cc3000_vbat')
		self.adafruit_cc3000_cs = config.getint(SECTION, 'adafruit_cc3000_cs')
		self.wlan_ssid = config.get(SECTION, 'wlan_ssid')
		self.wlan_pass = config.get(SECTION, 'wlan_pass')
		self.wlan_security = config.get(SECTION, 'wlan_security')
		# Parse optional parameters and assign default values.
		self.board_model = None
		if config.has_option(SECTION, 'board_model'):
			self.board_model = config.get(SECTION, 'board_model')
		self.arduino_dist = None
		if config.has_option(SECTION, 'arduino_dist'):
			self.arduino_dist = config.get(SECTION, 'arduino_dist')
		self.baud_rate = 115200
		if config.has_option(SECTION, 'baud_rate'):
			self.baud_rate = config.getint(SECTION, 'baud_rate')
		self.read_timeout_seconds = 60
		if config.has_option(SECTION, 'read_timeout_seconds'):
			self.read_timeout_seconds = config.getint(SECTION, 'read_timeout_seconds')


config = Configuration()
