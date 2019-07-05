from exceptions import InvalidContentType
from field import Field
from re import findall
from file import File


def parse_formdata(headers, data, file_func, field_func):
    """
    Function for parsing Multipart/Form-Data from response.
    Every key, value is decoded with 'UTF-8' except file data,
    it remains as binary.

    :param headers: Headers parsed from response.
    :param data: Data parsed from response.
    :param file_func: Callback function for handling file data, provided argument is File class.
    :param field_func: Callback function for handling regular field data, provided argument is Field class.
    """
    headers = headers["content-type"].split(";")
    content_type = headers[0]
    if content_type != "multipart/form-data":
        raise InvalidContentType("Content type must be multipart/form-data.")
    boundary = headers[1].replace(" boundary=", "")
    data = data.split(bytes("--" + boundary, "utf-8"))
    for value in data:
        if b"filename=" in value:
            try:
                field_name = findall(b' name="([\S\s]*?)"', value)[0].decode()
                field_filename = findall(b'filename="([\S\s]*?)"', value)[0].decode()
                field_content = findall(b'Content-Type: ([\S\s]*?)\r\n', value)[0].decode()
                field_data = value[value.index(b'\r\n\r\n')+4:-2]
                new_file = File(field_name, field_filename, field_content, field_data, content_type)
                file_func(new_file)
            except IndexError:
                pass
        else:
            try:
                field_name = findall(b' name="([\S\s]*?)"', value)[0].decode()
                field_data = value[value.index(b'\r\n\r\n')+4:-2].decode()
                new_field = Field(field_name, field_data, content_type)
                field_func(new_field)
            except IndexError:
                pass


def parse_xxx(headers, data, field_func):
    """
    Function for parsing application/x-www-form-urlencoded from response.
    There is no file callback function because file is handled like a regular field
    on application/x-www-form-urlencoded content type.

    :param headers: Headers parsed from response.
    :param data: Data parsed from response.
    :param field_func: Callback function for handling regular field data, provided argument is Field class.
    """
    content_type = headers["content-type"]
    if content_type != "application/x-www-form-urlencoded":
        raise InvalidContentType("Content type must be application/x-www-form-urlencoded.")
    data = data.split(b'&')
    for value in data:
        try:
            value = value.split(b'=')
            field_name = value[0].decode()
            field_data = value[1].decode()
            new_field = Field(field_name, field_data, content_type)
            field_func(new_field)
        except IndexError:
            pass


def parse_get(url, field_func):
    """
    Function for parsing data from GET response.
    Parses data directly from URL with splitting,
    format of key/values is 'UTF-8'.

    :param url: Requested URL from HTTP request.
    :param field_func: Callback function for handling regular field data, provided argument is Field class.
    """
    try:
        data = url.split("?")[1].split("&")
        for value in data:
            value = value.split("=")
            field_name = value[0]
            field_data = value[1]
            new_field = Field(field_name, field_data)
            field_func(new_field)
    except IndexError:
        pass


class ParseHttp:

    """
    Class for parsing HTTP request/response.
    """

    headers = {}  # Dictionary for storing all recieved headers.
    request = ""  # Full request as string. ex. "GET /login HTTP/1.1"
    method = ""  # HTTP request/response method. ex. "POST"
    body = b''  # Recieved data, all after headers is parsed as response data.
    http = ""  # HTTP version. ex. "HTTP/1.1"
    uri = ""  # Requested page/uri. ex. "/login"
    url = ""  # Full requested url (used for parsing GET data). ex. "/login?key=value"

    def __init__(self, conn):
        """
        Assigns provided socket object to 'self.conn' and starts parsing function.
        :param conn: Socket object for recieving HTTP data.
        """
        self.conn = conn
        self.parse_data()

    def parse_data(self):
        """
        Initially it listens on 'self.conn' socket
        for data with length of 10240 Bytes (10KB). After it parses headers it searches
        for 'Content-Length' in headers. If content length is bigger than recieved data
        it recieves in While loop till it recieves all data. After that it stores all data
        to 'self.body' as bytes data. It is not decoded right away because response may be
        raw file data which will trow error when decoded.
        """
        data = self.conn.recv(10240)
        if data != b'':
            if b'\r\n\r\n' in data:
                temp_data = data[:data.index(b'\r\n\r\n')].split(b'\r\n')
                self.request = temp_data[0].decode().split(" ")
                self.method = self.request[0]
                self.url = self.request[1]
                self.http = self.request[2]
                self.uri = self.url.split("?")[0]
                for header in temp_data[1:]:
                    header = header.decode()
                    key = header.split(": ")[0].lower()
                    try:
                        value = header.split(": ")[1]
                    except IndexError:
                        value = ""
                    self.headers[key] = value
            if self.method != "GET":
                if "content-length" in self.headers:
                    content_length = int(self.headers["content-length"])
                else:
                    content_length = len(data)
                while len(data) < content_length:
                    data = data + self.conn.recv(10240)
            self.body = data[data.index(b'\r\n\r\n')+4:]

    def get_headers(self):
        """
        :return: Parsed headers. Type: dictionary
        """
        return self.headers

    def get_method(self):
        """
        :return: Request/response method. Type: string
        """
        return self.method

    def get_url(self):
        """
        :return: Requested url. Type: string
        """
        return self.url

    def get_http(self):
        """
        :return: HTTP version. Type: string
        """
        return self.http

    def get_uri(self):
        """
        :return: Request/response method. Type: string
        """
        return self.uri

    def get_request(self):
        """
        :return: Requested path. Type: string
        """
        return self.request

    def get_body(self):
        """
        :return: Parsed data. Type: binary string
        """
        return self.body

    def __repr__(self):
        return "<ParseHttp {}>".format(self.conn)
