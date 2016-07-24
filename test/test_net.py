"""
Tests for Net interface module

It requires requests-mock
"""
import unittest

import requests_mock

import net
requests_mock.Mocker.TEST_PREFIX = 'test_'


@requests_mock.Mocker()
class NetInterfaceTests(unittest.TestCase):

    def test_make_get_request(self, mocker):
        mocker.register_url('GET', 'http://test.com', content='Hello world')
        r = net._make_get_request('https://test.com')
        self.assertEqual('Hello world', r.content)
