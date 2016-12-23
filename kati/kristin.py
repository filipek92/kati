#!/usr/bin/env python3

import requests
import logging
import functools


# Kristin API endpoint
KRISTIN_URL = "https://kristin.buk.cvut.cz/api/v1/penetrate/{reader}/{card}"

# communication timeout
TIMEOUT = 2

# cache size for access checks
CACHE_SIZE = 64

# start logger
logging.captureWarnings(True)  # log HTTP errors
log = logging.getLogger(__name__)


@functools.lru_cache(maxsize=CACHE_SIZE)
def has_access(reader_id, card_number):
    """
    Verify the access for given reader and card.

    :param reader_id: reader id
    :type reader_id: int
    :param card_number: card number
    :type card_number: int
    :return: True if access is granted, False otherwise
    :rtype: bool
    :raises: requests.exceptions.RequestException
    """
    # make request (with SSL check turned off)
    url = KRISTIN_URL.format(reader=reader_id, card=format_card_number(card_number))

    try:
        request = requests.get(url, verify=False, timeout=TIMEOUT)
        request.raise_for_status()
        res = request.json()["result"]

        # log result
        res_text = "granted" if res else "denied"
        log.info("access %s for card ID 0x%s at reader ID %s", res_text, format_card_number(card_number), reader_id)

    except requests.exceptions.RequestException:
        log.exception("access check failed")
        res = False

    return res


def format_card_number(data):
    """
    Format card number.

    :param data: card number
    :type data: int
    :return: card number in HEX format
    :rtype: str
    """
    return "{:014x}".format(data)
