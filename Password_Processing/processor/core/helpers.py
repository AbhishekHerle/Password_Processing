from __future__ import division
from processor import Sampling

class Helpers:

	def __init__(self):
		self._results = {}

	# TODO implement per pattern processing stats.
	def calculateProcessingStats(self, matchFile, unmatchFile, umCount, mCount):

		if mCount > 0:
			if mCount <= 10: X = mCount
			else: X = 10

			match = Sampling(X, matchFile).getRandomN()

		else: match = None

		if umCount > 0:
			if umCount <=10: Y = umCount
			else: Y = 10

			unmatch = Sampling(Y, unmatchFile).getRandomN()

		else: unmatch = None


		total = umCount + mCount
		umPercent = (umCount/total) * 100
		mPercent = (mCount/total) * 100

		return match, unmatch, total, umPercent, mPercent

	# Converts data to be returned into a dict
	def toDict(self, **kwargs):

		for key, val in kwargs.items():
			self._results[key] = val

		return self._results

