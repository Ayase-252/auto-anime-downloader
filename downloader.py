"""
Downloader

This module defines function to download torrent from Internet
"""
import os
from datetime import date

import net


def download(url, name, ep, translation_team='', save_path='', **kargs):
    """
    Download file from url

    params:
    url:                url of torrent
    name:               Name of anime
    ep:                 Episode number
    translation_team:   Translation team name
    save_path:          Path where the file will be saved

    return
    Full path of downloaded torrent
    """
    print('Downloading {} {} from {}'.format(name, ep, url))
    new_name = name + '-ep.' + str(ep) + '.torrent'
    new_path = save_path + date.today().strftime('%Y-%m-%d') + '/'
    try:
        net.download(url, new_name, new_path)
        print('File is saved at ', new_path + new_name)
        return new_path + new_name
    except Exception as ex:
        print(
            'Download is ternimated due to following exception:\n{}'.format(ex))
