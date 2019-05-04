import json
from django.views.decorators.csrf import csrf_exempt

from core.helpers import *
from core.decorator import pp_json_response
from core.exceptions import DisallowedMethod, ProcessingException
from core.processor import *

@csrf_exempt	# TODO Remove @csrf_exempt later on
@pp_json_response	# Decorator to return results as JSON responses

# Handles majority of the processing. Takes in a POST request containing the file to be processed and
# a list of GROK patterns to be applied to the data in the input file.
def doProcessing(request):

	try:

		if request.method != 'POST': raise DisallowedMethod

		else:
			p = Processor(request)
			matchFile, unmatchFile, mCount, umCount = p.beginProcessing()

			# TODO implement per pattern processing stats.
			match, unmatch, total, umPercent, mPercent = Helpers().calculateProcessingStats(matchFile, unmatchFile, umCount, mCount)
			return Helpers().toDict(match_results=match, unmatched_results=unmatch, total_number_of_lines=total, percentage_of_lines_matched=mPercent, percentage_of_lines_unmatched=umPercent)
	except Exception as e:
		raise

@csrf_exempt # TODO Remove @csrf_token
@pp_json_response

# Handles requests from sampling. Sampling provide a way for users to take a peek into the file.
# Primary objective is to take a look at the file and determine the sort of GROK patterns that will
# fit the need.
def getSample(request):

	try:

		if request.method != 'POST': raise DisallowedMethod

		else:
			sampleList = None

			r = Request(request)
			fileName = r.extractFileName()
			N, sampleType = r.getSamplingParams()

			s = Sampling(N, fileName)

			# Fetch random N lines from the file.
			if sampleType.lower() == 'random':
				sampleList = s.getRandomN()

			# Fetch last N lines from the input file.
			elif sampleType.lower() == 'last':
				sampleList = s.getLastN()

			# Fetch first N lines from the input file.
			elif sampleType.lower() == 'first':
				sampleList = s.getFirstN()

			else: raise KeyNotFoundException

			return Helpers().toDict(number_of_samples_requested = N, sample_type_requested = sampleType, sample_results = sampleList)

	except Exception as e:
		raise
