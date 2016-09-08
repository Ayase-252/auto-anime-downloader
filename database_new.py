"""Manage CRUD operations on database."""
import tinydb
from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware

from date_serializer import DateSerializer

DATABASE = 'anime.db'


def change_database(database):
    """Change database.

    Change DATABASE value in this module, then all operations will be performed
    on this database. This method can only be used on test.

    Args:
        database: Database name
    """
    global DATABASE
    DATABASE = database


def _opendb():
    """Open TinyDB database.

    Returns:
        Instance of TinyDB
    """
    serialization = SerializationMiddleware()
    serialization.register_serializer(DateSerializer(), 'Date Serializer')
    return tinydb.TinyDB(DATABASE, storage=serialization)


def save(table, instance):
    """Save instance in table.

    Args:
        table: Table name.
        instance: Instance of model. Model should implement toDict method.
    """
    db = _opendb()
    dbtable = db.table(table)
    dbtable.insert(instance.toDict())
    db.close()


def query(table, instance=None):
    """Retrieve instance(s) from table.

    Args:
        table: Table name.
        instance: Instance of model. Used as query condition.


    Returns:
        Dictionary of retrieved instance if instance is in this table. None if
        instance cannot be found in the table. List of all record in the table
        in dictionary if instance is None.
    """
    db = _opendb()
    dbtable = db.table(table)
    if instance is None:
        result = dbtable.all()
        db.close()
        return result
    else:
        origin = instance.toDict()
        query_condition = {key: origin[key]
                           for key in origin if origin[key] != ''}

        #  Query on TinyDB doesn't support a dictionary as condition.
        #  I have to implement one.
        instances = dbtable.all()
        db.close()

        def is_matched(instance):
            nonlocal query_condition
            for key in query_condition:
                if instance[key] != query_condition[key]:
                    return False
            return True
        result = list(filter(is_matched, instances))[0]
        return result


def update(table, instance, new_instance):
    """Update instance from table.

    Args:
        table: Table name.
        instance: Instance of model you want to update.
        new_instance: New instance of model.
    """
    pass


def remove(table, instance):
    """Remove instance from table.

    Args:
        table: Table name.
        instance: Instance of model you want to remove.
    """
    pass
