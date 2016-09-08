import unittest
import os

from tinydb import Query

import database_new as database


class TestModel:

    def __init__(self, attr_1='', attr_2=''):
        self.attr_1 = attr_1
        self.attr_2 = attr_2

    def toDict(self):
        return {
            'attr_1': self.attr_1,
            'attr_2': self.attr_2
        }


class DatabaseNewTests(unittest.TestCase):

    def setUp(self):
        database.change_database('Test.db')
        self.db = database._opendb()

    def tearDown(self):
        self.db.close()
        os.remove('Test.db')

    def test_save(self):
        test_instance = TestModel('hello', 'world')
        database.save('TestModel', test_instance)

        instance = Query()
        result = self.db.table('TestModel').get(instance.attr_1 == 'hello')
        self.assertEqual(result, {
            'attr_1': 'hello',
            'attr_2': 'world'
        })

    def test_query_with_instance(self):
        test_instance = TestModel('hello', 'world')
        another_instance = TestModel('another', 'world')
        database.save('TestModel', test_instance)
        database.save('TestModel', another_instance)

        query_instance = TestModel('hello')
        result = database.query('TestModel', query_instance)
        self.assertEqual(result, {
            'attr_1': 'hello',
            'attr_2': 'world'
        })

    def test_query_without_instance(self):
        test_instance_1 = TestModel('hello', 'world')
        test_instance_2 = TestModel('another', 'instance')
        database.save('TestModel', test_instance_1)
        database.save('TestModel', test_instance_2)

        result = database.query('TestModel')
        self.assertIn({
            'attr_1': 'hello',
            'attr_2': 'world'
        }, result)
        self.assertIn({
            'attr_1': 'another',
            'attr_2': 'instance'
        }, result)

    def test_update(self):
        old_instance = TestModel('hello', 'world')
        new_instance = TestModel('another', 'instance')
        database.save('TestModel', old_instance)

        database.update('TestModel', old_instance, new_instance)
        table = self.db.table('TestModel')
        self.assertEqual(len(table), 1)
        self.assertIn({
            'attr_1': 'another',
            'attr_2': 'instance'
        }, table.all())

    def test_remove(self):
        instance = TestModel('hello', 'world')
        database.save('TestModel', instance)

        database.remove('TestModel', instance)
        table = self.db.table('TestModel')
        self.assertEqual(len(table), 0)
