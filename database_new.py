"""Manage CRUD operations on database."""
import tinydb
from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware

from date_serializer import DateSerializer


def opendb(database):
    """Open TinyDB database.

    Args:
        database: Database name

    Returns:
        Instance of TinyDB
    """
    serialization = SerializationMiddleware()
    serialization.register_serializer(DateSerializer(), 'Date Serializer')
    return tinydb.TinyDB(database, storage=serialization)


def save(database, object):
    """Save object in database.

    Args:
        database: Database name.
        object: Object of model. Model should implement toDict method.
    """
    pass


def query(database, object=None):
    """Retrieve object(s) from database.

    Args:
        database: Database name.
        object: Object of model. Used as query condition.


    Returns:
        Dictionary of retrieved object if object is in database. None if object
        cannot be found in database. List of all record in database in
        dictionary if object is None.
    """
    pass


def update(database, object, new_object):
    """Update object from database.

    Args:
        database: Database name.
        object: Object of model you want to update.
        new_object: Object of model containing new information
    """
    pass


def remove(database, object):
    """Remove object from database.

    Args:
        database: Database name.
        object: Object of model you want to remove.
    """
    pass
