import BaseTestCase

class BuildTest(BaseTestCase.BaseTestCase):
	def verifyOutput(self, output):
		self.assertRegexpMatches(output, 'Locating time server...')
		self.assertRegexpMatches(output, 'connected!')
		self.assertRegexpMatches(output, 'Awaiting response...OK')
		self.assertRegexpMatches(output, 'Current UNIX time: \d+ ')

	def getSketchPath(self):
		return "./InternetTime"
