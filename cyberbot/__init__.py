import datetime
import platform
import socket
import sys

from .cogs import *
from .exceptions import *
from .managers import *
from .setup import *
from .config import *

def version():
    return "v0.1.0-alpha"


def config_version():
    return "0.1"


def time():
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")


def year():
    return str(datetime.datetime.now().year)


def copyright():
    if year() == "2022":
        return "© 2022 ProgNeo"
    else:
        return f"© 2022-{year()} ProgNeo"


def getPlatform():
    return platform.system() + " " + platform.release()


def hostname():
    return socket.gethostname()


def ip():
    return socket.gethostbyname(hostname())


def path():
    return sys.path