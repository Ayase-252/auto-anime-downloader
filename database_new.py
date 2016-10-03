"""Perform CRUD operations on database."""
import tinydb
from tinydb import Query
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
        Element of TinyDB
    """
    serialization = SerializationMiddleware()
    serialization.register_serializer(DateSerializer(), 'Date Serializer')
    return tinydb.TinyDB(DATABASE, storage=serialization)


def save(table, element):
    """Save element in table.

    Args:
        table: Table name.
        element: Element of model. Model should implement toDict method.
    """
    db = _opendb()
    dbtable = db.table(table)
    dbtable.insert(element.to_dict())
    db.close()


def query(table, element=None):
    """Retrieve element(s) from table.

    Args:
        table: Table name.
        element: Element of model. Used as query condition.


    Returns:
        Dictionary of retrieved element if element is in this table. None if
        element cannot be found in the table.
    """
    db = _opendb()
    dbtable = db.table(table)
    if element is None:
        result = dbtable.all()
        db.close()
        return result
    else:
        origin = element.to_dict()
        query_condition = {key: origin[key]
                           for key in origin if origin[key] != ''}

        #  Query on TinyDB doesn't support a dictionary as condition.
        #  I have to implement one.
        elements = dbtable.all()
        db.close()

        def is_matched(element):
            nonlocal query_condition
            for key in query_condition:
                if element[key] != query_condition[key]:
                    return False
            return True
        result = list(filter(is_matched, elements))[0]
        return result


def queryAll(table):
    """Get all elements from table.

    Args:
        table: Table name.

    Returns:
        List of all elements of table.
    """
    pass


def update(table, element, new_element):
    """Update element from table.

    Args:
        table: Table name.
        element: Element of model you want to update.
        new_element: New element of model.
    """
    db = _opendb()
    dbtable = db.table(table)

    old_element = element.to_dict()
    Element = Query()
    element = dbtable.get(Element[element.primary_key]
                          == old_element[element.primary_key])
    dbtable.update(new_element.to_dict(), eids=[element.eid])
    db.close()


def remove(table, element):
    """Remove element from table.

    Args:
        table: Table name.
        element: Element of model you want to remove.
    """
    db = _opendb()
    dbtable = db.table(table)

    old_element = element.to_dict()
    Element = Query()
    element = dbtable.remove(Element[element.primary_key]
                             == old_element[element.primary_key])
    db.close()
