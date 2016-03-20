#!/usr/bin/env python3

import requests
import logging


# Kristin API endpoint
KRISTIN_URL = 'https://kristin.buk.cvut.cz/api/v1/penetrate/{reader}/{card}'

# communication timeout
TIMEOUT = 3

# log HTTP errors
logging.captureWarnings(True)


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
    request = requests.get(url, verify=False, timeout=TIMEOUT)
    request.raise_for_status()

    return request.json()['result']


def format_card_number(data):
    """
    Format card number.

    :param data: card number
    :type data: int
    :return: card number in HEX format
    :rtype: str
    """
    return '{:014x}'.format(data)
