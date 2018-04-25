"""
Generic logger
"""

import sys
import logging
from .conf import Config

__log_levels = {
    "CRITICAL": 50,
    "ERROR": 40,
    "WARNING": 30,
    "INFO": 20,
    "DEBUG": 10,
    "NOTSET": 0
}

__root = logging.getLogger()
__root.setLevel(__log_levels[Config.get("logger_level", "DEBUG")])

__ch = logging.StreamHandler(sys.stdout)
__ch.setLevel(__log_levels[Config.get("logger_level", "DEBUG")])
__formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
__ch.setFormatter(__formatter)
__root.addHandler(__ch)

Log = __root
