"""
Downloader

This module defines function to download torrent from Internet
"""
from urllib import request
import os


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
    response = request.urlopen(url)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    f = open(save_path + name + '-ep.' + str(ep) + '-' +
             '.torrent', 'wb')
    f.write(response.read())
