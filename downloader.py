"""
Downloader

This module defines function to download torrent from Internet
"""
from urllib import request


def download(file_meta, save_path=''):
    """
    Download file from url provided by filemeta.

    Param:
    file_meta:    An object of FileMeta class indicating the meta of file
    save_path:  Path where the file will be saved
    """
    print('Downloading {0} from {1}'.format(file_meta.name, file_meta.url))
    response = request.urlopen(file_meta.url)
    f = open(save_path + file_meta.name + '-ep.' + str(file_meta.ep) + '-' +
             '.torrent', 'wb')
    f.write(response.read())
