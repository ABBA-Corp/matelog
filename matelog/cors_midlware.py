from django.utils.deprecation import MiddlewareMixin


class CustomCorsMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def process_request(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = "*"

        print(response.headers)

        # Code to be executed for each request/response after
        # the view is called.

        return response
