import logging
import sys

from config import CONSOLE_LOG_SEVERITY

severity = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger (using a StreamHandler - logs to stdout)

    :param name: Name of the logger
    :return: logging.Logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(severity[CONSOLE_LOG_SEVERITY])
    formatter = logging.Formatter(
        "%(asctime)s [%(name)s] %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    logger.propagate = False
    return logger
