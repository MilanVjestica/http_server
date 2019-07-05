
"""
Custom exceptions. Class name explains it.
"""


class InvalidFileType(Exception):

    def __init__(self, message):
        super().__init__(message)


class FieldExists(Exception):

    def __init__(self, message):
        super().__init__(message)


class CookieExists(Exception):

    def __init__(self, message):
        super().__init__(message)


class InvalidCode(Exception):

    def __init__(self, message):
        super().__init__(message)


class RuleExists(Exception):

    def __init__(self, message):
        super().__init__(message)


class InvalidArgumentName(Exception):

    def __init__(self, message):
        super().__init__(message)


class LoopExit(Exception):

    def __init__(self, message):
        super().__init__(message)


class InvalidRuleArg(Exception):

    def __init__(self, message):
        super().__init__(message)


class RuleFunctionNone(Exception):

    def __init__(self, message):
        super().__init__(message)


class InvalidContentType(Exception):

    def __init__(self, message):
        super().__init__(message)
