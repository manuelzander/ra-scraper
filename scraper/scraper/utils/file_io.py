import os

import pandas as pd

from config import PROJECT_ROOT
from scraper.utils.logger import get_logger

log = get_logger(__name__)


def get_artists(filename):
    try:
        with open(os.path.join(PROJECT_ROOT, filename), "r") as file:
            lines = [line.strip() for line in file.readlines()]
        # file.seek(0)
        # file.close()
        log.info("File %s read and artists %s extracted", filename, lines)
        return lines
    except Exception as e:
        log.error("Unexpected ERROR: %s", e)
        raise SystemExit


def get_data(filename):
    try:
        data = pd.read_json(os.path.join(PROJECT_ROOT, filename), lines=True)
        log.info("File %s read and JSONL data extracted", filename)
        return data
    except Exception as e:
        log.error("Unexpected ERROR: %s", e)
        raise SystemExit
