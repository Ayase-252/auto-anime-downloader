from datetime import date, datetime

import tinydb

DEFAULT_DATABASE = 'bangumi.db'


def opendb():
    """
    Open TinyDB database

    warning:
    parameter dbname is only designed for unit test.
    PASSING AN ARGUMENT VIA dbname is forbidden.
    """
    return tinydb.TinyDB(DEFAULT_DATABASE)


def add_bangumis(bangumi_list):
    """
    Add bangumis provided by bangumi_list into database

    param:
    bangumi_list    list of objects of Bangumi class
    """
    db = opendb()
    blist = [bangumi.dict() for bangumi in bangumi_list]
    db.insert(bangumi_list)
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
    q = tinydb.Query()
    result = db.search(
        (date.today()
         - datetime.strptime('%Y-%m-%d', q.start_date).total_seconds()
         // timedelta(days=1).total_seconds()
         // 7) > q.dled_ep)
    db.close()
