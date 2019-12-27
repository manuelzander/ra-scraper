import requests

from scraper.utils.logger import get_logger

log = get_logger(__name__)


def get_request(url, data, headers, session=None):
    if session is None:
        response = requests.get(url, data=data, headers=headers)
    else:
        response = session.get(url, data=data, headers=headers)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        log.error("ERROR: GET request: %s: %s", e, response.json())
        raise SystemExit
    except Exception as e:
        log.error("Unexpected ERROR: %s %s", type(e).__name__, e.args[0])
        raise SystemExit
    else:
        log.debug("SUCCESS: GET request")
        return response


def post_request(url, data, headers, session=None):
    if session is None:
        response = requests.post(url, data=data, headers=headers)
    else:
        response = session.post(url, data=data, headers=headers)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        log.error("ERROR: POST request: %s: %s", e, response.json())
        raise SystemExit
    except Exception as e:
        log.error("Unexpected ERROR: %s %s", type(e).__name__, e.args[0])
        raise SystemExit
    else:
        log.debug("SUCCESS: POST request")
        return response


def delete_request(url, headers, session=None):
    if session is None:
        response = requests.delete(url, headers=headers)
    else:
        response = session.delete(url, headers=headers)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        log.error("ERROR: DELETE request: %s: %s", e, response.json())
        raise SystemExit
    except Exception as e:
        log.error("Unexpected ERROR: %s %s", type(e).__name__, e.args[0])
        raise SystemExit
    else:
        log.debug("SUCCESS: DELETE request")
        return response


def put_request(url, data, headers, session=None):
    if session is None:
        response = requests.put(url, data=data, headers=headers)
    else:
        response = session.put(url, data=data, headers=headers)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        log.error("ERROR: PUT request: %s: %s", e, response.json())
        raise SystemExit
    except Exception as e:
        log.error("Unexpected ERROR: %s %s", type(e).__name__, e.args[0])
        raise SystemExit
    else:
        log.debug("SUCCESS: PUT request")
        return response
