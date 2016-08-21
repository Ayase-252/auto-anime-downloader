"""
Utorrent Adaptor

This module uses utorrent WebAPI to manage the process of download.
"""
import re

import requests
from requests.auth import HTTPBasicAuth

import configure

# Present token
_TOKEN = ''
_COOKIES = {}


def add_torrent(torrent_path, file_subpath):
    """
    Add torrent to utorrent via WebAPI

    params:
    file_subpath    Relative path from download path which designated in
                    utorrent

    Warning:
    According to document, string in Unicode cannot be handled correctly.
    Avoid to use unicode character here.
    """
    params = {
        'action': 'add-file',
        'token': _TOKEN,
        'download_dir': 1,
        'path': file_subpath
    }
    files = {
        'torrent_file': open(torrent_path, 'rb')
    }
    r = _make_request(params=params, files=files, method='POST')
    if r.status_code != 200:
        raise RuntimeError(
            'Adding torrent failed with status code ' + str(r.status_code))


def is_token_initialized():
    """
    Return whether token is initialized
    """
    return _TOKEN is not ''


def refresh_token():
    """
    Get token via WebAPI

    Utorrent implements a token authentication system to prevent CSRF.
    Refer to https://github.com/bittorrent/webui/wiki/TokenSystem

    All actions requires a token which is hidden in /gui/token.html
    """
    global _TOKEN, _COOKIES
    response = _make_request(path='/gui/token.html')
    reg = re.compile(r"<div id='token' style='display:none;'>(.+)</div>")
    _TOKEN = reg.search(response.text).group(1)
    _COOKIES['GUID'] = response.cookies['GUID']


def _make_request(*, headers={}, params={}, files={}, path='/gui/', method='GET'):
    """
    Make request to url while authentication is handled.

    params:
    All parameters is required to pass via named argument

    url     URL of Destination
    params  Payload carried by url
    method  Method of request

    return:
    Response of request
    """
    username = configure.WEBAPI_USERNAME
    password = configure.WEBAPI_PASSWORD
    port = configure.WEBAPI_PORT

    url = 'http://127.0.0.1:' + str(port) + path

    function_table = {
        'GET': requests.get,
        'POST': requests.post
    }

    if method == 'GET':
        return requests.get(url,
                            params=params,
                            headers=headers,
                            cookies=_COOKIES,
                            auth=HTTPBasicAuth(username, password))
    elif method == "POST":
        return requests.post(url,
                             params=params,
                             headers=headers,
                             cookies=_COOKIES,
                             auth=HTTPBasicAuth(username, password),
                             files=files)
