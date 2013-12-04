import BaseTestCase

class BuildTest(BaseTestCase.BaseTestCase):
	def verifyOutput(self, output):
		self.assertRegexpMatches(output, 'This is a test of the CC3000 module!\nIf you can read this, its working :\)')
		self.assertRegexpMatches(output, 'Disconnecting')

	def getSketchPath(self):
		return "./WebClient"
