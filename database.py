from datetime import date, timedelta

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
    db.close()


def update(bangumi):
    """
    Update bangumi information in database

    param:
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
        now_air_episode = (date.today()
                           - bangumi['start_date']).total_seconds() \
            / timedelta(days=1).total_seconds() // 7
        for i in range(bangumi['dled_ep'] + 1, int(now_air_episode) + 1):
            unloaded_episodes.append(FileMeta(name=bangumi['name'],
                                              ep=i,
                                              translation_team=bangumi[
                                                  'translation_team'],
                                              url=''))
    return unloaded_episodes
