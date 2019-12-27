from scraper.utils.logger import get_logger
from config import PROJECT_ROOT
import os

log = get_logger(__name__)


def get_artists(filename):
    try:
        with open(os.path.join(PROJECT_ROOT, filename), "r") as file:
            lines = [line.strip() for line in file.readlines()]
        # file.seek(0)
        # file.close()
        log.info("File %s read - artists extracted %s", filename, lines)
        return lines
    except Exception as e:
        log.error("Unexpected ERROR: %s", e)
        raise SystemExit
