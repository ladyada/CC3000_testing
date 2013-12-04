import BaseTestCase

class BuildTest(BaseTestCase.BaseTestCase):
	def verifyOutput(self, output):
		self.assertRegexpMatches(output, 'Connected!')
		self.assertRegexpMatches(output, 'Ping successful!')
		self.assertRegexpMatches(output, 'Closing the connection')

	def getSketchPath(self):
		return "./buildtest"
