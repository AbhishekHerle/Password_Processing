import json
import random
import subprocess
import io
from queue import Queue
from threading import Thread
from pygrok import Grok

from models import Pattern, File
from exceptions import EmptyBodyException, ProcessingException, FileProcessingException

# Class to process the HTTP requests and extract all necessary parameters.
class Request:
	def __init__(self, request):

		if request.body != '': self._params = json.loads(request.body)
		else: raise EmptyBodyException

		self._P = []
		self._N = 100
		self._sampleOptions = ('last', 'first', 'random')
		self._sampleType = None

	def extractPatterns(self):
		try:
			patterns = self._params['patterns']
			for k, v in patterns.items():
				self._P.append(Pattern(k, v))

			return self._P

		except:
			raise ProcessingException

	def extractFileName(self):
		try:
			return self._params['file_name']
		except:
			raise ProcessingException

	def getSamplingParams(self):
		try:
			if "N" in self._params.keys(): self._N = self._params['N']
			print(self._params['sampleType'].lower())
			if self._params['sampleType'].lower() in self._sampleOptions: self._sampleType = self._params['sampleType']
			else: raise ValueError("{0} is not a valid value".format(self._params['sampleType']))

			return self._N, self._sampleType.lower()

		except Exception as e:
			raise

# Class containing the methods necessary to fetch lines from a file.
class Sampling:

	def __init__(self, N, fileName):
		self._N = int(N)
		self._fileName = fileName
		self._sampleList = []

	def getFirstN(self):
		try:
			with open(self._fileName) as f:
				self._sampleList = [(x, next(f).strip()) for x in range(self._N)]

			return self._sampleList

		except:
			raise ProcessingException

	# Reservior Sampling using N as the reservior size
	def getRandomN(self):
		try:
			with open(self._fileName) as f:
				for i, line in enumerate(f):
					if i < self._N:
						self._sampleList.append((i, line.strip()))
					else:
						m = random.randint(0,i)
						if m < self._N: self._sampleList[m] = (i, line.strip())

			return self._sampleList

		except:
			raise ProcessingExecption

	# Linux's 'tail' being used to fetch last N lines.
	# TODO find a Platform independent method
	def getLastN(self):
		try:
			tail = 'tail -n {0} {1}'.format(str(self._N).decode("latin-1"), self._fileName)
			proc = subprocess.Popen(tail.split(' '), stdout=subprocess.PIPE)
			self._sampleList = [ (i, line.strip()) for i, line in enumerate(proc.stdout.readlines())]

			return self._sampleList

		except:
			raise ProcessingException

# Contains methods to perfom pattern matching. Processing is multithreaded and makes use of a Producer
# thread that puts lines to be processed into a Queue and a Consumer thread processes the items in the
# Queue.
class Processor:
	def __init__(self, request):
		self._R = Request(request)
		self._P = self._R.extractPatterns()
		self._fileName = self._R.extractFileName()
		self._F = File(self._fileName)
		self._matchFile, self._unmatchFile = self._F.getPostProcessingFileNames()


		self._M = None
		self._UM = None

		self._umCount = 0
		self._mCount = 0

		self._fileData = []

	# Consumer Method.
	def startConsumer(self, Q):
		try:
			while True:

				text = Q.get()
				notMatch = True

				# Go through each pattern to see if it matches the line.
				# If the line matches a pattern, break out of the for loop as
				# there is no need to search for another match 
				for p in self._P:

					g = Grok(p._pattern)
					ans = g.match(text)

					if ans != None:

						# Write into <filename>_match.txt if there is a pattern match
						# TODO find a way around the encoding issues
						notMatch = False
						ptext = ' '.join([x.encode("latin-1") + ':'.encode("latin-1") + y.encode("latin-1") for x, y in ans.items()])
						self._M.write(ptext.decode("latin-1") + ' '.decode("latin-1") + p.getTag().decode("latin-1") + '\n'.decode("latin-1"))

						self._mCount = self._mCount + 1

						break

				# If there is no match write into <filename>_unmatch.txt
				if notMatch == True:
					self._UM.write(text)
					self._umCount = self._umCount + 1

				Q.task_done()

		except:
			raise ProcessingException

	# Start the Producer thread to feed the lines into the Queue
	def beginProcessing(self):
		try:
			Q = Queue()

			self._M = io.open(self._matchFile, 'w+', encoding="latin-1")
			self._UM = io.open(self._unmatchFile, 'w+', encoding="latin-1")

			t = Thread(target=self.startConsumer, args=(Q,))
			t.daemon = True
			t.start()

			with io.open(self._fileName, 'r', encoding="latin-1") as f:
				for text in f:
					Q.put(text)

			Q.join()
			self.closeAllFiles()

			return self._matchFile, self._unmatchFile, self._mCount, self._umCount

		except:
			raise ProcessingException

	# Close all files
	def closeAllFiles(self):
		try:
			self._M.close()
			self._UM.close()
		except:
			raise FileProcessingException

# TODO In progress
class PreProcess:
	def __init__(self, fileName, tempFile, N=None):
		self._N = N
		self._fileName = fileName
		self._tempFile = tempFile

	def removeFirstN(self):
		try:
			with io.open(self._fileName, 'r') as infile, io.open(self._tempFile, 'w') as outfile:
				for i in range(self._N):
					infile.next()
				for line in infile:
					outfile.write(line)

		except:
			raise FileProcessingException
