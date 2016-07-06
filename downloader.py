"""
Downloader

This module defines function to download torrent from Internet
"""
from urllib import request


def download(filemeta, save_path=''):
    """
    Download file from url provided by filemeta.

    Param:
    filemeta:    An object of FileMeta class indicating the meta of file
    save_path:  Path where the file will be saved
    """
    response = request.urlopen(filemeta.url)
    f = open(save_path + filemeta.name + '-ep.' + str(filemeta.ep) + '-' +
             filemeta.translation_group + '.torrent', 'wb')
    f.write(response.read())
