from exceptions import FieldExists, \
                       InvalidCode, \
                       CookieExists


class Header:

    """
    Header object for modifying header data that will be sent to client.
    """

    codes = {
        100: "Continue",
        101: "Switching Protocols",
        102: "Processing",
        200: "OK",
        201: "Created",
        202: "Accepted",
        203: "Non-authoritative Information",
        204: "No Content",
        205: "Reset Content",
        206: "Partial Content",
        207: "Multi-Status",
        208: "Already Reported",
        226: "IM Used",
        300: "Multiple Choices",
        301: "Moved Permanently",
        302: "Found",
        303: "See Other",
        304: "Not Modified",
        305: "Use Proxy",
        307: "Temporary Redirect",
        308: "Permanent Redirect",
        400: "Bad Request",
        401: "Unauthorized",
        402: "Payment Required",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        406: "Not Acceptable",
        407: "Proxy Authentication Required",
        408: "Request Timeout",
        409: "Conflict",
        410: "Gone",
        411: "Length Required",
        412: "Precondition Failed",
        413: "Payload Too Large",
        414: "Request-URI Too Long",
        415: "Unsupported Media Type",
        416: "Requested Range Not Satisfiable",
        417: "Expectation Failed",
        418: "I'm a teapot",
        421: "Misdirected Request",
        422: "Unprocessable Entity",
        423: "Locked",
        424: "Failed Dependency",
        426: "Upgrade Required",
        428: "Precondition Required",
        429: "Too Many Requests",
        431: "Request Header Fields Too Large",
        444: "Connection Closed Without Response",
        451: "Unavailable For Legal Reasons",
        499: "Client Closed Request",
        500: "Internal Server Error",
        501: "Not Implemented",
        502: "Bad Gateway",
        503: "Service Unavailable",
        504: "Gateway Timeout",
        505: "HTTP Version Not Supported",
        506: "Variant Also Negotiates",
        507: "Insufficient Storage",
        508: "Loop Detected",
        510: "Not Extended",
        511: "Network Authentication Required",
        599: "Network Connect Timeout Error"
    }  # All codes and their message used for response.

    code = ""
    header = {}  # Stores all headers that will be sent to client.
    cookies = {}  # Stores all provided cookies to be sent with 'Set-Cookie'.

    def add_field(self, key=None, value=None, override=True):
        """
        Add field to headers dictionary.

        :param key: Header key. ex. 'Content-Type'
        :param value: Header value. ex. 'text/html'
        :param override: Whether to override header if it is in headers dictionary.
        :return: True for success. Exception(FieldExists) if key is in headers and override is False.
        """
        if key not in self.header or override is True:
            self.header[key] = value
            return True
        raise FieldExists("Key is in header. To override it set arg override to True.")

    def add_cookie(self, key=None, value=None, override=True):
        """
        Adds cookie to be stored in clients browser(or program) with 'Set-Cookie' header.

        :param key: Cookie key. ex. 'session'
        :param value: Cookie value. ex. 'user1'
        :param override: Whether to override cookie.
        :return: True for succes. Exception(CookieExists) if cookie exists and override is False.
        """
        if key not in self.cookies or override is True:
            self.cookies[key] = value
            return True
        raise CookieExists("Cookie already exists. To override it set arg override to True.")

    def rem_cookie(self, key):
        """
        Remove cookie from cookies dictionary.

        :param key: Cookie key. ex. 'session'
        :return: True for success. Exception(KeyError) if cookie isn't in cookies dict.
        """
        if key in self.cookies:
            self.cookies.pop(key)
            return True
        raise KeyError

    def rem_field(self, key):
        """
        Remove header from headers dictionary.

        :param key: Header key. ex. 'Content-Type'
        :return: True for success. Exception(KeyError) if header isn't in headers dict.
        """
        if key in self.header:
            self.header.pop(key)
            return True
        raise KeyError

    def set_code(self, code):
        """
        Set response code.

        :param code: Response code.
        :return: True for success. Exception(InvalidCode) if code is invalid (not in 'self.codes' dict)
        """
        if code in self.codes:
            self.code = "HTTP/1.1 {} {}".format(code, self.codes[int(code)])
            return True
        raise InvalidCode("Invalid code.")

    def clr_cookie(self):
        """
        Clear cookie dictionary.

        :return: True for success.
        """
        self.cookies.clear()
        return True

    def clr_header(self):
        """
        Clear headers dictionary.

        :return: True for success.
        """
        self.header.clear()
        return True

    def clear(self):
        """
        Clear all dictionaries.

        :return: True for success.
        """
        self.header.clear()
        self.cookies.clear()
        return True

    def __call__(self):
        """
        Return all headers and add cookies to 'Set-Cookie' header.
        Returns as string and is later encoded if needed.

        :return: Headers as string.
        """
        cks = ""
        for key in self.cookies:
            cks += "{}={};".format(key, self.cookies[key])
        if cks != "":
            self.add_field("Set-Cookie", cks)
        hdr = ""
        for key in self.header:
            hdr += "{}: {}\r\n".format(key, self.header[key])
        self.clear()
        return "{}\r\n{}\r\n".format(self.code, hdr)
