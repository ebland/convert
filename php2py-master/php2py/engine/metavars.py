import os.path
from typing import Any

from php2py.phpbaselib import filters
from php2py.phpbaselib.specials import Specials
from php2py.phpbaselib.functions import Functions
from .basetypes import PhpBase
from php2py.phpbaselib.PDO import PDO


class PhpVars(object):
    def init_vars(self, app: "PhpApp") -> None:
        self.__init__()
        self.app = app
        self.g = app.g
        self.f = app.f
        self.c = app.c
        self.constants = app.constants

    def __getattribute__(self, name):
        """ Apparently getattr is called after first searching to see if there is already an attribute attr

        I think we have to do this because php eats undefined variables for breakfast

        """
        try:
            return super().__getattribute__(name)
        except:
            return None


class PhpFunctions(PhpVars, Specials, Functions):
    pass


class PhpGlobals(PhpVars):
    def __init__(self) -> None:
        # Sets the super-global variables
        # $_POST etc
        self._SERVER = {}
        self._GET = {}
        self._POST = {}
        self._COOKIES = {}
        self._REQUEST = {}
        # TODO: implement getitem and setitem so GLOBALS global works
        # Or just convert as part of transformer...
        self.GLOBALS = self


class PhpClasses(PhpVars):
    def __init__(self) -> None:
        self.PhpBase = PhpBase
        self.PDO = PDO

    def __setattr__(self, key: str, value: Any) -> None:
        super().__setattr__(key.lower(), value)

    def __getattribute__(self, item: str) -> Any:
        return super().__getattribute__(item.lower())


class PhpConstants(PhpVars):
    def __init__(self) -> None:
        self.PHP_VERSION = "5.4.0"

        self.DIRECTORY_SEPARATOR = os.path.sep

        # Error reporting constants
        # TODO: Maybe we should just always be something like E_ALL...
        self.E_ERROR            = 1    # Fatal errors. Exit
        self.E_WARNING          = 2    # Run time errors. Don't exit
        self.E_PARSE            = 4    # Parse errors.
        self.E_NOTICE           = 8    # Run time notices. Might or might not be an actual error
        self.E_CORE_ERROR       = 16   # Errors on startup in the core
        self.E_CORE_WARNING     = 32   # Errors at startup which aren't fatal
        self.E_COMPILE_ERROR    = 64   # Fatal compile time errors
        self.E_COMPILE_WARNING  = 128  # Compile time non fatal errors
        self.E_USER_ERROR       = 256  # Fatal user error generated by trigger_error function
        self.E_USER_WARNING     = 512  # Not fatal...
        self.E_USER_NOTICE      = 1024 # Just a notice
        self.E_STRICT           = 2048 # Enables suggestions from php engine
        self.E_RECOVERABLE_ERROR= 4096 # Probably dangerous? Like an exception I think
        self.E_DEPRECATED       = 8192 # Indicated deprecated functionality at run time
        self.E_USER_DEPRECATED  = 16384
        self.E_ALL              = 32797 # All errors and warnings

        self.FILTER_SANITIZE_URL = filters.filter_sanitize_url


def init_metavars(app: "PhpApp"):
    _f_.init_vars(app)
    _g_.init_vars(app)
    _c_.init_vars(app)
    _constants_.init_vars(app)

# Php meta variables. These singletons need to be reset before every serve
_f_ = PhpFunctions()
_g_ = PhpGlobals()
_c_ = PhpClasses()
_constants_ = PhpConstants()