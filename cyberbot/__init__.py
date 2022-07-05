import datetime
import platform
import socket
import sys

from .cogs import *
from .exceptions import *
from .managers import *
from .setup import *
from .config import *
from .helpers import *
from .events import *
    
def version() -> str:
    return "v0.2.1-alpha"


def config_version() -> str:
    return "0.1"


def time() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")


def year():
    return str(datetime.datetime.now().year)


def copyright() -> str:
    if year() == "2022":
        return "© 2022 ProgNeo"
    else:
        return f"© 2022-{year()} ProgNeo"


def getPlatform() -> str:
    return platform.system() + " " + platform.release()


def hostname() -> str:
    return socket.gethostname()


def ip() -> str:
    return socket.gethostbyname(hostname())


def path() -> str:
    return sys.path