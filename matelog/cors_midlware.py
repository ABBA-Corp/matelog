from django.utils.deprecation import MiddlewareMixin


class CustomCorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = "https://meta-logistic.vercel.app"
        response["Access-Control-Allow-Headers"] = "multipart/form-data, Access-Control-Allow-Origin, ru"
        response['Access-Control-Allow-Methods'] = "GET, HEAD, PUT, PATCH, POST, DELETE"
        response["Access-Control-Allow-Credentials"] = 'https://meta-logistic.vercel.app'

        print(response.headers)

        # Code to be executed for each request/response after
        # the view is called.

        return response
