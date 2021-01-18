"""
Default logging module for Yasna
"""
import logging

from os import environ

FORMAT = "%(asctime)s %(levelname)s %(filename)s %(message)s"
logging.basicConfig(format=FORMAT)
logger = logging.getLogger("yasna.main")
logger.setLevel(environ.get("LOGLEVEL", "INFO"))


def get_logger(name):
    """
    return a logger
    """
    return logging.getLogger(name)
