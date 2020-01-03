import mimetypes
import os
from email.mime.text import MIMEText

import pandas as pd

from config import PROJECT_ROOT
from scraper.utils.logger import get_logger

log = get_logger(__name__)


def get_artists(filename):
    try:
        with open(os.path.join(PROJECT_ROOT, filename), "r") as file:
            lines = [line.strip() for line in file.readlines()]
        log.info("File %s read and artists %s extracted", filename, lines)
        return lines
    except Exception as e:
        log.error("Unexpected ERROR: %s", e)
        raise SystemExit


def get_data(filename):
    try:
        data = pd.read_json(os.path.join(PROJECT_ROOT, filename), lines=True)
        log.info("File %s read and JSONL data extracted for Email body", filename)
        return data
    except Exception as e:
        log.error("Unexpected ERROR: %s", e)
        raise SystemExit


def get_attachement(filename):
    path = os.path.join(PROJECT_ROOT, filename)
    ctype, encoding = mimetypes.guess_type(path)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    try:
        with open(path) as file:
            attachement = MIMEText(file.read(), _subtype=subtype, _charset='utf-8')
        log.info("File %s read and JSONL data extracted for Email attachement", filename)
        return attachement
    except Exception as e:
        log.error("Unexpected ERROR: %s", e)
        raise SystemExit