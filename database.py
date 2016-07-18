from datetime import date, timedelta, datetime
from math import ceil

import tinydb
from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware

from date_serializer import DateSerializer
from filemeta import FileMeta

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
        '{0} bangumi/s has been insert into database.'.format(
            len(bangumi_list)
        )
    )
    db.close()


def update(bangumi):
    """
    Update bangumi information in database

    params:
    bangumi         object of Bangumi class
    """
    db = opendb()
    q = tinydb.Query()
    db.update(bangumi.dict(), q.name == bangumi.name)
    db.close()


def unloaded_episodes():
    """
    Fetch undownloaded episodes

    return:
    list of dict of filemeta
    """
    db = opendb()
    bangumi = tinydb.Query()
    unloaded_bangumi = db.search(bangumi.next_onair_date <= date.today())
    db.close()
    unloaded_episodes = []
    for bangumi in unloaded_bangumi:
        start_date = bangumi['start_date']
        start_date_datetime = datetime(
            start_date.year, start_date.month, start_date.day)
        now_air_episode = ceil((datetime.now()
                                - start_date_datetime).total_seconds()
                               / timedelta(days=1).total_seconds() / 7)
        print('Bangumi info: {0}'.format(bangumi['name']))
        print('Time interval to next on air day: {0}'.format(
            (datetime.now() - start_date_datetime).total_seconds()))
        print('Calculated days to next on air day: {0}'.format((datetime.now() - start_date_datetime
                                                                ).total_seconds() / timedelta(days=1).total_seconds()))
        print('Available episode:{0}'.format(now_air_episode))
        for i in range(bangumi['dled_ep'] + 1, int(now_air_episode) + 1):
            unloaded_episodes.append(FileMeta(name=bangumi['name'],
                                              ep=i,
                                              translation_team=bangumi[
                                                  'translation_team'],
                                              url=''))
    return unloaded_episodes


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
    bangumi_info['dled_ep'] += 1
    db.update(bangumi_info, bangumi.name == bangumi_name)
