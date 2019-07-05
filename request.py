

class Request:

    """
    Class for storing all HTTP request/response data.
    """

    uri = ""  # Requested path
    url = ""  # Full requested url
    get = {}  # GET data
    http = ""  # HTTP version
    post = {}  # POST data
    files = {}  # All recieved files
    method = ""  # HTTP method
    cookies = {}  # Cookies
    headers = {}  # Headers
    boundary = ""  # Boundary for parsing data

    def clear(self):
        """
        Returns all values to empty.
        """
        self.uri = ""
        self.url = ""
        self.get = {}
        self.http = ""
        self.post = {}
        self.data = []
        self.files = {}
        self.method = ""
        self.cookies = {}
        self.headers = {}
        self.boundary = ""
