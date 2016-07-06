import unittest
import os
from datetime import date, timedelta

import tinydb

import database
from filemeta import FileMeta


class DatabaseTestClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        database.DEFAULT_DATABASE = 'test.db'
        db = tinydb.TinyDB('test.db')
        bangumi_dict = [
            {
                'name': 'test bangumi 2',
                'translation_group': ['sumisora'],
                'start_date': (date.today() + timedelta(days=1)).isoformat(),
                'cached_ep': 0,
                'total_ep': 12,
                'offset': 0
            },
            {
                'name': 'test bangumi 3',
                'translation_group': ['sumisora'],
                'start_date': (date.today() - timedelta(days=47)).isoformat(),
                'cached_ep': 7,
                'total_ep': 13,
                'offset': 0
            }
        ]
        db.insert_multiple(bangumi_dict)
        db.close()

    @classmethod
    def tearDownClass(cls):
        os.remove('test.db')

    def test_unloaded_episode(self):
        unloaded_episodes = database.unloaded_episodes()
        intended_episodes = [FileMeta('test bangumi 2', 8, 'sumisora')]
        for intended_episode in intended_episodes:
            self.assertIn(intended_episode, unloaded_episodes)
