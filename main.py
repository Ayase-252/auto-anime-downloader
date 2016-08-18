"""
Main module

This module contains methods to response user input
"""
import json

import database
import bangumi
import downloader
import configure
import scraper


def main():
    """
    Scan database and retrieve torrents from remote servers

    usage:
    py aad.py
    """
    print('Importing scrapers')
    scrapers = scraper.import_scrapers()
    print('Caculating available episodes')
    avail_episode = database.fetch_available_episodes()
    if len(avail_episode) == 0:
        print('No episode is available at present')
        return
    print('These episodes are available:')
    for ep in avail_episode:
        print('{} of {}'.format(ep['ep'], ep['name']))
    print('Download starts:')
    for ep in avail_episode:
        print('Ep.{} of {} is processing'.format(ep['ep'], ep['name']))
        for scraper in scraper:
            try:
                url = dmhy.get_download_url(**ep)
                downloader.download(url=url,
                                    save_path=configure.TORRENT_SAVE_PATH,
                                    **ep)
                database.set_downloaded_episode(ep['name'], ep['ep'])
                break
            except FileNotFoundError:
                print('Scraper cannot find the file')
            # If last scraper is used
            if scraper is scrapers[-1]:
                print('File cannot be found in all scraper. Try next time.')


def update(file_path):
    """
    Update database with JSON file

    usage:
    py aad.py update file_path

    param:
    file_path        Path to JSON file
    """
    f = open(file_path, 'r', encoding='utf-8')
    parsed = json.loads(f.read(), encoding='utf-8')
    f.close()
    for anime in parsed:
        database.update_anime_info(
            anime['name'],
            bangumi.parsed_json_to_new_dict(anime)
        )


def add(file_path):
    """
    Add entries to database with JSON file

    usage:
    py aad.py add file_path

    param:
    file_path       Path to JSON file
    """
    animes = bangumi.read_bangumi_from_file(file_path)
    database.add_bangumis(animes)


def check_database():
    """
    Check constraints in database

    usage:
    py aad.py check
    """
    print('Program is checking data in the database. Any data violating '
          'constraints will be removed from database.')
    database.remove_finished_anime()
    print('Data checking is completed.')
