"""
Downloader

This module defines function to download torrent from Internet
"""
import os

import requests


def download(url, name, ep, translation_team='', save_path='', **kargs):
    """
    Download file from url

    params:
    url:                URL of torrent
    name:               Name of anime
    ep:                 Episode number
    translation_team:   Translation team name
    save_path:          Path where the file will be saved
    """
    print('Downloading {} {} from {}'.format(name, ep, url))
    user_agent = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML,'
                      'like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    }
    response = requests.get(url, headers=user_agent, timeout=5)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    f = open(save_path + name + '-ep.' + str(ep) + '-' +
             '.torrent', 'wb')
    f.write(response.content)
    f.close()
