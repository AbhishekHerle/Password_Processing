class BasePpException(Exception):

    # Base class of PP-based exceptions inherited by all other exceptions

    _message = ''
    _http_status = 500

    def get_message(self):
        return self._message

    def get_http_status(self):
        return self._http_status

class EmptyBodyException(BasePpException):

    # Thrown when the request has an empty body

    _message = "Request has an empty body"
    _http_status = 406

class DisallowedMethod(BasePpException):

    # Thrown when the request method used is not allowed (a request method other than GET)

    _message = "Request method not allowed"
    _http_status = 405

class ProcessingException(BasePpException):

    # Generic processing exception.

    _message = "Error during Processing"
    _http_status = 500

class FileProcessingException(BasePpException):

    # Generic file processing exception

	_message = "Error Processing File(s)"
	_http_status = 409
