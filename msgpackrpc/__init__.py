import sys

inPy3k = sys.version_info[0] == 3

from pkg_resources import get_distribution, DistributionNotFound

try:
    version = get_distribution("msgpackrpc").version
except DistributionNotFound:
    version = "trunk"

__version__ = version

# shortcut for most-used symbols
from msgpackrpc.loop import Loop
from msgpackrpc.client import Client
from msgpackrpc.server import Server
from msgpackrpc.address import Address
