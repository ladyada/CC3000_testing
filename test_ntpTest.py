import BaseTestCase

class BuildTest(BaseTestCase.BaseTestCase):
	def verifyOutput(self, output):
		self.assertRegexpMatches(output, 'Current local time is:\r\n\d+:\d+:\d+.\d+')
		self.assertRegexpMatches(output, 'Day of year: \d+')
		self.assertRegexpMatches(output, 'Closing the connection')

	def getSketchPath(self):
		return "./ntpTest"
