"""
Default logging module for Yasna
"""
import logging
import re

from os import environ

FORMAT = "%(asctime)s %(levelname)s %(filename)s %(message)s"
logging.basicConfig(format=FORMAT)
logger = logging.getLogger("yasna.main")
logger.setLevel(environ.get("LOGLEVEL", "INFO"))


class SanitizeFormatter(object):
    """
    SanitizeFormatter
    """

    def __init__(self, orig_formatter):
        self.orig_formatter = orig_formatter

    def format(self, record):
        """
        Removes any special character from
        the log message to prevent any malicious
        code that could help to make commands
        """
        message = self.orig_formatter.format(record)
        message = re.sub(r"/[^A-Za-zñÑ0-9\s\.\,]*", "", message)
        return message

    def __getattr__(self, attr):
        return getattr(self.orig_formatter, attr)


for h in logging.root.handlers:
    h.setFormatter(SanitizeFormatter(h.formatter))


def get_logger(name):
    """
    return a logger
    """
    return logging.getLogger(name)
