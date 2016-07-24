"""
Tests for Net interface module

It requires requests-mock
"""
import unittest
import os

import requests_mock

import net
requests_mock.Mocker.TEST_PREFIX = 'test_'


@requests_mock.Mocker()
class NetInterfaceTests(unittest.TestCase):

    def test_make_get_request(self, mocker):
        mocker.register_uri('GET', 'http://test.com', text='Hello world')
        r = net._make_get_request('http://test.com')
        self.assertEqual('Hello world', r.text)

    def test_download(self, mocker):
        mocker.register_uri('GET', 'http://test.com', content=b'Hello world')
        net.download('http://test.com', 'test.file')
        f = open('test.file', 'rb')
        content = f.read()
        f.close()
        os.remove('test.file')
        self.assertEqual(b'Hello world', content)

    def test_request_get_content(self, mocker):
        mocker.register_uri('GET', 'http://test.com', content=b'<html></html>')
        content = net.request_get_content('http://test.com')
        self.assertEqual(b'<html></html>', content.content)

    def test_request_get_content_retry_fail(self, mocker):
        mocker.register_uri('GET', 'http://test.com',
                            text='Not found', status_code=404)
        self.assertRaises(RuntimeError,
                          net.request_get_content,
                          'http://test.com', 2, 0.1)
