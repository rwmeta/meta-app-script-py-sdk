class AuthError(Exception):
    def __init__(self, request):
        self.request = request

    def __str__(self):
        return repr(self.request)
