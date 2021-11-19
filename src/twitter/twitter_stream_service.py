import logging
from typing import List

import requests

from .twitter_auth import get_bearer_auth_header

URL_TWITTER_STREAM = "https://api.twitter.com/2/tweets/search/stream"


def get_rules():
    response = requests.get(
        f"{URL_TWITTER_STREAM}/rules",
        headers={**get_bearer_auth_header()},
    )
    if response.status_code != 200:
        message = "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        logging.error(message)
        raise Exception(message)

    logging.info(response.json())
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        f"{URL_TWITTER_STREAM}/rules",
        headers={**get_bearer_auth_header()},
        json=payload
    )
    if response.status_code != 200:
        message = f"Cannot delete rules (HTTP {response.status_code}): {response.text}"
        logging.error(message)
        raise Exception(message)

    logging.info(response.json())


def set_rules(rules: List[str] = None):
    # You can adjust the rules if needed
    payload = {"add": rules}
    response = requests.post(
        f"{URL_TWITTER_STREAM}/rules",
        headers={**get_bearer_auth_header()},
        json=payload,
    )
    if response.status_code != 201:
        message = "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        logging.error(message)
        raise Exception(message)

    logging.info(response.json())


def get_stream(set):
    response = requests.get(
        URL_TWITTER_STREAM,
        headers={**get_bearer_auth_header()},
        stream=True,
    )
    if response.status_code != 200:
        message = f"Cannot get stream (HTTP {response.status_code}): {response.text}"
        logging.error(message)
        raise Exception(message)

    all_streams = []
    for response_line in response.iter_lines():
        if response_line:
            json_response = response_line
            all_streams.append(json_response)
            logging.info(json_response)

    return all_streams
