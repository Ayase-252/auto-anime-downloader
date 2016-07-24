"""
Net interface module

The module provides methods to access internet resource such as obtaining web
content and download file. To keep all internet accesses coordinated, all codes
SHALL make them request via methods in this module
"""
import os
import time

import requests


def download(url, file_name, save_path=''):
    """
    Download file from location indicated by url, and save it in save_path

    params:
    url         Resource url
    file_name   Name of downloaded file
    save_path   Saving path of downloaded file
    """
    response = _make_get_request(url)
    if save_path != '' and not os.path.exists(save_path):
        os.makedirs(save_path)
    f = open(save_path + file_name, 'wb')
    f.write(response.content)
    f.close()


def request_get_content(url, retry=0, retry_interval=5):
    """
    Get content of response subject to request to url

    params:
    url             Resource url
    retry           Max retry time
    retry_interval  Time interval between retries
    """
    try_time = retry + 1
    r = None
    while r is None or r.status_code != 200:
        try:
            r = _make_get_request(url)
        except Exception as e:
            print('\n\nException raised\n', e)
        try_time -= 1
        if r.status_code != 200:
            print('Error: Request returns response with status code',
                  r.status_code)
        if try_time == 0:
            break
        print('Retry will starts in {} second'.format(retry_interval))
        time.sleep(retry_interval)
    if r is None or r.status_code != 200:
        raise RuntimeError(
            'Reach maximun retry time in requesting url {}'.format(url))
    else:
        return r


def _make_get_request(url, params=[]):
    """
    Make HTTP GET requests to assigned url and parameters

    params:
    url         Resource url
    params      Additional parameters bore by request

    return:
    response object returned by requests lib
    """
    default_headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML,'
                      'like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    }

    default_time_out = 10
    return requests.get(url, params=params,
                        headers=default_headers, timeout=default_headers)
