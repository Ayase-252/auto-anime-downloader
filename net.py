"""
Net interface module

The module provides methods to access internet resource such as obtaining web
content and download file. To keep all internet accesses coordinated, all codes
SHALL make them request via methods in this module
"""
import os
import time
from datetime import date

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


def request_get_content(url, retry=1, retry_interval=5, params=[]):
    """
    Get content of response subject to GET request to url

    params:
    url             Resource url
    retry           Max retry attempts including initial attempt
    retry_interval  Time interval between retries
    """
    try_time = retry
    r = None
    print('Retriving data from', url)
    while r is None or r.status_code != 200 and try_time != 0:
        try:
            r = _make_get_request(url, params)
        except Exception as e:
            print('\n\nException raised while connecting\n', e)
            print('Retry will starts in {} second'.format(retry_interval))
            try_time -= 1
            time.sleep(retry_interval)
            continue
        if r.status_code != 200:
            print('Error: Request returns response with status code',
                  r.status_code)
            print('Retry will starts in {} second'.format(retry_interval))
            try_time -= 1
            time.sleep(retry_interval)
            continue
    if r is None or r.status_code != 200:
        raise RuntimeError(
            'Reach maximun retry time in requesting url {}'.format(url))
    else:
        return r.content


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
                        headers=default_headers, timeout=default_time_out)


def download_torrent(url, name, ep,
                     translation_team='', save_path='', **kargs):
    """Download torrent on URL and save it.

    Args:
        url: Url of torrent.
        name: Name of anime.
        ep:  Episode number.
        translation_team: Translation team name.
        save_path: Path where the file will be saved.
        **kargs: Collect remaining keyword arguments.

    Returns:
        Full path of downloaded torrent.

    Raises:
        Exception: Whenever exception raised by download method or print, which
            is usually raised by encoding problem, the method will raise
            identical exception to caller.
    """
    print('Downloading {} {} from {}'.format(name, ep, url))
    new_name = name + '-ep.' + str(ep) + '.torrent'
    new_path = save_path + date.today().strftime('%Y-%m-%d') + '/'
    try:
        download(url, new_name, new_path)
        print('File is saved at ', new_path + new_name)
        return new_path + new_name
    except Exception as ex:
        print(
            'Download is ternimated due to following exception:\n{}'
            .format(ex))
        raise ex    # Transmit exception to upper layer
