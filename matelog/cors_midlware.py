from django.utils.deprecation import MiddlewareMixin


class CustomCorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        
        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = "http://localhost:3000"
        response["Access-Control-Allow-Headers"] = 'Content-Type, LNG1'
        response['Access-Control-Allow-Methods'] = "GET, HEAD, PUT, PATCH, POST, DELETE"
        response["Access-Control-Allow-Credentials"] = 'true'

        print(response.headers)

        # Code to be executed for each request/response after
        # the view is called.

        return response
