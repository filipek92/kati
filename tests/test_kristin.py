#!/usr/bin/env python3

import unittest
import re
import requests
import responses
from kati import kristin


class TestKristin(unittest.TestCase):

    def setUp(self):
        # expected URL pattern
        self.url = re.compile(
            r'^https://kristin.buk.cvut.cz/api/v1/penetrate/[0-9]+/[0-9a-fA-F]+$')

    @responses.activate
    def test_has_access(self):
        """Test successful access."""
        responses.add(responses.GET, self.url, json={'result': True})  # mock
        self.assertTrue(kristin.has_access(1, 1234567876543))

    @responses.activate
    def test_has_access_error(self):
        """Test communication error."""
        responses.add(responses.GET, self.url, status=500)  # mock
        with self.assertRaises(requests.exceptions.RequestException):
            kristin.has_access(1, 1234567876543)

    def test_format_card_number(self):
        """Test card number formatting."""
        fmt = kristin.format_card_number  # alias
        self.assertEquals(fmt(1234567876543), "00011f71facfbf")
        self.assertEquals(fmt(1234567323), "0000004996009b")
        self.assertEquals(fmt(1), "00000000000001")
        self.assertEquals(fmt(0), "00000000000000")
