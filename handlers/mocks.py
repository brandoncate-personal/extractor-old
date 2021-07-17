class Request:
    def __init__(self, args):
        self.args = args


class ResponseHeaders:
    def set(self, key, value):
        return


class Response:
    headers: ResponseHeaders

    def __init__(self):
        self.headers = ResponseHeaders()
