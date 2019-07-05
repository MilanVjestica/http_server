from exceptions import InvalidFileType, RuleExists, InvalidArgumentName, LoopExit
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from parsers import parse_formdata, parse_xxx, parse_get, ParseHttp
from string import ascii_letters, digits
from tzlocal import get_localzone
from datetime import datetime
from session import Session
from jinja2 import Template
from request import Request
from header import Header
from random import choice
from mime import Mime
from os import path

pages_folder = "./pages/"  # HTML data, scripts, stylesheets... Location

req = Request()
header = Header()
session = Session()


def render_template(file, **kwargs):
    """
    Render template with Jinja.

    :param file: HTML/HTM file. ex. 'index.html'
    :param kwargs: Arguments to be provided to Jinja function.
    :return: HTML page data for success. \
             Exception(FileNotFoundError) if file doesn't exist. \
             Exception(InvalidFileType) if file isn't HTML or HTM.
    """
    if file.endswith(".html") or file.endswith(".htm"):
        if path.isfile(pages_folder + file):
            header.set_code(200)
            with open(pages_folder + file, "r") as f:
                page = Template(f.read())
                f.close()
                header.add_field("Content-Type", Mime.types["." + file.split(".")[-1]])
                return page.render(**kwargs)
        header.set_code(404)
        return load_file("404.html").decode()
    raise InvalidFileType("Template file must be .html or .htm.")


def load_file(file):
    """
    Load data of the file and return it.

    :param file: File to be loaded.
    :return: File data for success. Exception(FileNotFoundError) if file doesn't exist.
    """
    header.set_code(200)
    if file == "":
        header.set_code(404)
        file = "/404.html"
    if file[0] == "/":
        file = file[1:]
    if path.isfile(pages_folder + file):
        if file.split(".")[-1] in Mime.images:
            with open(pages_folder + file, "rb") as f:
                header.add_field("Accept-Ranges", "bytes")
                data = f.read()
                f.close()
        else:
            with open(pages_folder + file, "r") as f:
                data = f.read().encode()
                f.close()
        header.add_field("Content-Type", Mime.types["." + file.split(".")[-1]])
        return data
    raise FileNotFoundError("File doesn't exist.")


def generate_cookie(length=32):
    """
    Generate session id to be send as cookie.

    :param length: Length of session id.
    :return: Session id.
    """
    keys = ascii_letters + digits + "-"
    return "".join(choice(keys) for _ in range(length))


def redirect(rule):
    """
    Redirect to some other page.

    :param rule: Path to redirect to.
    :return: HTML redirect meta tag.
    """
    return '''<head>
            <meta http-equiv="refresh" content="0; URL={}" />
        </head>
    '''.format(rule)


class Server(object):

    """
    Class for initiating, running, parsing, sending all needed data.
    'Brains of the operation' type class.
    """

    server_host = "127.0.0.1"  # Host for the server to listen
    server_port = 80  # Port for the server to listen
    server_reuse = True  # Reuse port and address

    rules = {}  # Rules for all paths

    info = False  # Wether to print all data that 'Server' class prints

    def start(self):
        """
        Create socket, assign it to 'self.sock'.
        Bind it and setup listening, after run handling function.
        """
        self.sock = socket(AF_INET, SOCK_STREAM)
        if self.server_reuse:
            self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.bind((self.server_host, self.server_port))
        self.sock.listen(10)
        self.print_info("Server started on {}:{}".format(self.server_host, self.server_port))
        self.handle_request()

    @staticmethod
    def get_field(field):
        """
        Callback function for 'parse_get' function.

        :param field: Field object.
        """
        req.get[field.get_field_name()] = field.get_file_data()

    @staticmethod
    def post_field(field):
        """
        Callback function for parsing POST data.

        :param field: Field object.
        """
        req.post[field.get_field_name()] = field.get_file_data()

    @staticmethod
    def post_file(file):
        """
        Callback function for parsing POST function.
        Stores all files in 'req.files' dictionary
        so it can be easly accessed by user.

        :param file: File object.
        """
        if file.get_field_name() not in req.files:
            req.files[file.get_field_name()] = []
        req.files[file.get_field_name()].append({
            "object": file,
            "filename": file.get_file_name(),
            "content_type": file.get_file_content_type()
        })

    def handle_request(self):
        """
        Listen for incoming connections and parse their request.
        """
        while True:
            conn, addr = self.sock.accept()
            self.parse_request(conn, ParseHttp(conn))

    def parse_request(self, conn, parser):
        """
        Function for parsing request, setting up headers and sending data.
        Works like magic btw.

        :param conn: Socket object of client.
        :param parser: Parser object.
        """
        req.clear()
        header.clear()
        req.headers = parser.get_headers()
        req.method = parser.get_method()
        req.uri = parser.get_uri()
        req.url = parser.get_url()
        req.http = parser.get_http()
        res_data = parser.get_body()
        self.print_info(parser.get_request())
        if "content-type" in req.headers:
            req.type = req.headers["content-type"].split(";")[0]
        if "cookie" in req.headers:
            cookies = req.headers["cookie"].split("; ")
            for cookie in cookies:
                if cookie != "":
                    cookie = cookie.split("=")
                    req.cookies[cookie[0]] = cookie[1].replace("\r", "")
            if "session" in req.cookies:
                session.init(req.cookies["session"])
            else:
                header.add_cookie("session", generate_cookie())

        if res_data is not b'':
            parse_get(req.url, self.get_field)
            if req.method == "POST":
                if req.type == "application/x-www-form-urlencoded":
                    parse_xxx(req.headers, res_data, self.post_field)
                elif req.type == "multipart/form-data":
                    parse_formdata(req.headers, res_data, self.post_file, self.post_field)
            if req.uri == "":
                req.uri = "/"
        if req.uri in self.rules:
            header.set_code(200)
            data = self.rules[req.uri]["function"]().encode()
        else:
            try:
                data = load_file(req.uri)
            except FileNotFoundError:
                fnd = False
                req_data = req.uri.split("/")
                while "" in req_data:
                    req_data.remove("")
                for rule in self.rules:
                    rule_data = rule.split("/")
                    while "" in rule_data:
                        rule_data.remove("")
                    var_indexes = []
                    variables = {}
                    for dat in rule_data:
                        if "<" in dat and ">" in dat:
                            var_indexes.append(rule_data.index(dat))
                    try:
                        for index in sorted(var_indexes, reverse=True):
                            variables[rule_data[index]] = req_data[index]
                            req_data.pop(index)
                            rule_data.pop(index)
                        if req_data == rule_data:
                            kwargs = {}
                            for var in variables:
                                value = variables[var]
                                var = var.replace("<", "").replace(">", "").split(":")
                                try:
                                    kwargs[var[1]] = eval("{}(\"{}\")".format(var[0], value))
                                except ValueError:
                                    raise LoopExit
                            header.set_code(200)
                            try:
                                data = str(self.rules[rule]["function"](**kwargs)).encode()
                            except TypeError:
                                raise InvalidArgumentName("Argument name and variable rule don't match.")
                            fnd = True
                            break
                    except (TypeError, NameError, LoopExit):
                        pass
                if fnd is False:
                    header.set_code(404)
                    header.add_field("Content-Type", "text/html")
                    data = load_file("/404.html")
        now = datetime.now(get_localzone())
        header.add_field("Keep-Alive", "timeout=5, max=99")
        header.add_field("Date", now.strftime("%a, %d %b %Y %H:%M:%S %Z"))
        header.add_field("Content-Length", len(data))
        data_to_send = header().encode() + data
        conn.send(data_to_send + b'\r\n')

    def print_info(self, info):
        """
        Print to terminal if 'self.info' is True.

        :param info: Data to print.
        """
        if self.info:
            print(info)

    def add_rule(self, rule=None, function=None, methods=None):
        """
        Add rule to 'self.rules'.

        :param rule: Rule path. ex. '/login'
        :param function: Rule function. ex. 'login_handle'
        :param methods: This doesn't work so far so don't use it.
        :return: True for success. Exception(RuleExists) if rule is in 'self.rules' dictionary.
        """
        if rule not in self.rules:
            self.rules[rule] = {}
            self.rules[rule]["function"] = function
            self.rules[rule]["methods"] = methods
            return True
        raise RuleExists("Rule already exists.")

    def path(self, rule=None, methods=None):
        """
        Decorator for 'self.add_rule' function.
        Rule function is autmatically obtained.

        :param rule: Rule path. ex. '/login'
        :param methods: This doesn't work so far so don't use it.
        """
        def decorator(f):
            self.add_rule(rule, f, methods)
            return f
        return decorator

    def __repr__(self):
        return "<HTTP Server [{}:{}]>".format(self.server_host, self.server_port)
