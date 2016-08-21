from datetime import date, timedelta, datetime
from math import ceil

import tinydb
from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware

from date_serializer import DateSerializer

DEFAULT_DATABASE = 'bangumi.db'


def opendb():
    """
    Open TinyDB database
    """
    serialization = SerializationMiddleware()
    serialization.register_serializer(DateSerializer(), 'Date Serializer')
    return tinydb.TinyDB(DEFAULT_DATABASE, storage=serialization)


def add_bangumis(bangumi_list):
    """
    Add bangumis provided by bangumi_list into database

    param:
    bangumi_list    list of bangumis
    """
    db = opendb()
    db.insert_multiple(bangumi_list)
    print(
        '{0} bangumi/s has been inserted into database.'.format(
            len(bangumi_list)
        )
    )
    db.close()


def set_downloaded_episode(bangumi_name, episode):
    """
    Set downloaded episode record of sepcified bangumi

    params:
    bangumi_name        Name of bangumi
    episode             Episode number
    """
    db = opendb()
    bangumi = tinydb.Query()
    bangumi_info = db.get(bangumi.name == bangumi_name)
    bangumi_info['dled_ep'] = episode
    db.update(bangumi_info, bangumi.name == bangumi_name)

# IDEA: Change name to get_avail_episodes


def fetch_available_episodes():
    """
    Fetch available episodes at the time when the function is called

    return:
    list of dict of available episode(s)
    """
    db = opendb()
    animes = db.all()
    db.close()
    if len(animes) == 0:
        print('There is no animes in database')
        return []
    avail_episodes = []
    for anime in animes:
        print('anime: {0}'.format(anime['name']))
        start_date = anime['start_date']
        start_date_datetime = datetime(
            start_date.year, start_date.month, start_date.day)
        time_interval = datetime.now() - start_date_datetime
        time_interval_days = time_interval.total_seconds() \
            / timedelta(days=1).total_seconds()
        episode_now = int(ceil(time_interval_days / 7)) - anime['offset']
        print('days between now and start day:{0}'.format(time_interval_days))
        print('episode available now:{}'.format(episode_now))
        print('downloaded:{}\n\n'.format(anime['dled_ep']))
        if episode_now > anime['dled_ep']:
            for i in range(anime['dled_ep'] + 1, episode_now + 1):
                avail_episodes.append({
                    'name': anime['name'],
                    'keyword': anime['keyword'],
                    'translation_team': anime['translation_team'],
                    'ep': i,
                    'folder': anime['folder']
                })
    return avail_episodes


def update_anime_info(name, new):
    """
    Update information of anime with a dict contains new information

    params:
    name        Name of anime you want to update
    new         A dict contains new infomation, the value whose key name starts
                with new_ will replaces the corresponding item
    """
    db = opendb()
    anime = tinydb.Query()
    info = db.get(anime.name == name)
    print('\nUpdating {}:'.format(name))
    for key in new:
        if key.startswith('new_'):
            new_key = key[4:]
            info[new_key] = new[key]
            print('{} is replaced with {}'.format(new_key, new[key]))
    db.update(info, anime.name == name)
    db.close()


def remove_anime(name):
    """
    Remove anime from database

    params:
    name    Name of anime you want to remove
    """
    db = opendb()
    anime = tinydb.Query()
    db.remove(anime.name == name)
    db.close()
    print('{} is removed from database'.format(name))


def remove_finished_anime():
    """
    Remove finished anime in the database
    """
    db = opendb()
    anime_group = db.all()
    count = 0
    for anime in anime_group:
        if anime['total_ep'] == anime['dled_ep']:
            remove_anime(anime['name'])
            count += 1
    print('{} anime is(are) removed form database'.format(count))
    db.close()


def get_anime_by_name(name):
    """
    param:
    name        Name of anime
    return:
    dict contains all information
    """
    db = opendb()
    anime = tinydb.Query()
    r = db.get(anime.name == name)
    db.close()
    return r


def get_all_anime():
    """
    return:
    dict contains all anime in the database
    """
    db = opendb()
    anime_group = db.all()
    return anime_group
