import BaseTestCase

class GeoLocation(BaseTestCase.BaseTestCase):
	def verifyOutput(self, output):
		self.assertRegexpMatches(output, 'Connecting to geo server...')
		self.assertRegexpMatches(output, 'Reading response...OK')
		self.assertRegexpMatches(output, 'Disconnecting')
		self.assertRegexpMatches(output, 'RESULTS:')
		self.assertRegexpMatches(output, 'Longitude: [-.\d]+')
		self.assertRegexpMatches(output, 'Latitude: [-.\d]+')

	def getSketchPath(self):
		return "./GeoLocation"
