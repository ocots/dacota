"""
    Errors description
"""


class Error(Exception):
    """
    This exception is the generic class
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class ArgumentTypeError(Error):
    """
    This exception may be raised when one argument of a function has a wrong type
    """


class ArgumentDimensionError(Error):
    """
    This exception may be raised when one array argument of a function has not consistent dimensions with respect to others parameters
    """


class InputArgumentError(Error):
    """
    This exception may be raised when the number of input arguments is wrong
    """


class OptionNameError(Error):
    """
    This exception may be raised when one tries to get an option which does not exist
    """
