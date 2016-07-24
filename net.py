"""
Net interface module

The module provides methods to access internet resource such as obtaining web
content and download file. To keep all internet accesses coordinated, all codes
SHALL make them request via methods in this module
"""

import requests


def download(uri, file_path):
    """
    Download file from location indicated by uri, and save it in file_path

    params:
    uri         Resource uri
    file_path   Path of downloaded file
    """
    pass


def _make_get_request(uri, params=[]):
    """
    Make HTTP GET requests to assigned uri and parameters

    params:
    uri         Resource uri
    params      Additional parameters bore by request
    """
    default_headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML,'
                      'like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    }

    default_time_out = 10
    return requests.get(uri, params=params,
                        headers=default_headers, timeout=default_headers)
