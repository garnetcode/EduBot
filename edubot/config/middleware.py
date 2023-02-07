class CustomMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)
        try:
            print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            if request.path not in ["/admin/jsi18n/"] and "Django" not in response.content.decode():
                print("RECEIVED REQUEST: " + request.path)
                print("REQUEST METHOD: " + request.method)
                print("RESPONSE STATUS IN MIDDLEWARE : ", response.status_code)
                print("SENDING BACK THIS RESPONSE : ", response.content)
                print(
                    "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
        except Exception as e:
            print("EXCEPTION IN MIDDLEWARE : ", e) if " This FileResponse instance has no `content` attribute. Use `streaming_content` instead" not in str(
                e) else None

        # Code to be executed for each request/response after
        # the view is called.
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        pass

    def process_template_response(self, request, response):
        # Code to be executed for each request/response after
        # the view is called.
        print
        return response

    def process_exception(self, request, exception):
        # Code to be executed for each request/response after
        # the view is called.
        pass

    def process_template_response(self, request, response):
        # Code to be executed for each request/response after
        # the view is called.
        return response

    def process_response(self, request, response):
        # Code to be executed for each request/response after
        # the view is called.
        return response
