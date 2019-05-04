import uuid
import os

# Pattern model
class Pattern:
	def __init__(self, name, pattern):
		self._pattern = pattern
		self._name = name
		self._count = 0

	# Associate a matched line with the pattern that matched it
	def getTag(self):
		return "matched:" + self._name

# Model to handle file name generation
class File:
	def __init__(self, name):
		self._name = name
		self._tempFile = os.path.splitext(os.path.basename(self._name))[0] + str(uuid.uuid4()) + ".txt"
		self._matchFile = os.path.splitext(os.path.basename(self._name))[0] + "_matched" + ".txt"
		self._unmatchFile = os.path.splitext(os.path.basename(self._name))[0] + "_unmatched"  + ".txt"

	def getTempFile(self):
		return self._tempFile

	def getPostProcessingFileNames(self):
		return self._matchFile, self._unmatchFile
