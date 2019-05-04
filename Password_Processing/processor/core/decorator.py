import time
from django.http import JsonResponse
from exceptions import BasePpException

# Decorator to return results as JSON responses
def pp_json_response(func):

    def func_wrapper(*args, **kwargs):
        try:
            time_start = time.time()
            data = func(*args, **kwargs)
            time_end = time.time()
            result = {
                'results': data,
                'duration': float('{0:.4f}'.format(time_end - time_start))
            }
            status = 200

        except Exception as e:
            status = 503
            error_message = '{}'.format(e)

            if isinstance(e, BasePpException):
                error_message = e.get_message()
                status = e.get_http_status()

            result = {
                'message': '{}: {}'.format(status, error_message)
            }

        return JsonResponse(result, safe=False, status=status)

    return func_wrapper
