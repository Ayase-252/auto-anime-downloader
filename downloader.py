"""
Downloader

This module defines function to download torrent from Internet
"""
from urllib import request


def download(bangumi, save_path=''):
    """
    Download file from url with provided bangumi info.

    Param:
    bangumi:    An object of Bangumi class indicating the meta of file
    save_path:  Path where the file will be saved
    """
    response = request.urlopen(bangumi.url)
    f = open(save_path + bangumi.name + '-ep.' + str(bangumi.ep) + '-' +
             bangumi.translation_group + '.torrent', 'wb')
    f.write(response.read())
