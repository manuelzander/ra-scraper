import os

CONSOLE_LOG_SEVERITY = "INFO"

from scraper.utils.logger import get_logger

log = get_logger(__name__)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    def __init__(self):
        self.ACCOUNT = self._get_key_or_fail("ACCOUNT")
        self.SECRET = self._get_key_or_fail("SECRET")

    @staticmethod
    def _get_key_or_fail(key):
        if key in os.environ:
            return os.environ.get(key)
        else:
            msg = f"{key} is not set in the environment and is required for the runtime"
            log.error(msg)
            raise KeyError(msg)
