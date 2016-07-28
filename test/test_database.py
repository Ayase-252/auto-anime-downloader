import unittest
import os
from datetime import date, timedelta

import tinydb

import database


class FetchAvailableEpisodesTests(unittest.TestCase):
    """
    Test class to test fetch_available_episodes
    """

    def setUp(self):
        """
        Configure database for test purposes. Remind to close db after data
        insertion.
        """
        database.DEFAULT_DATABASE = 'test.db'
        self.db = database.opendb()

    def tearDown(self):
        os.remove('test.db')

    def test_function_1(self):
        """
        Test function in situation where only one is available
        """
        anime_dict = [{
            'name': 'test bangumi 2',
            'keyword': 'test bangumi 2',
            'translation_team': ['sumisora'],
            'start_date': date.today() + timedelta(days=1),
            'dled_ep': 0,
            'total_ep': 12,
            'offset': 0
        }, {
            'name': 'test bangumi 3',
            'keyword': 'test bangumi 3',
            'translation_team': ['sumisora'],
            'start_date': date.today() - timedelta(days=49),
            'dled_ep': 6,
            'total_ep': 13,
            'offset': 0
        }
        ]
        self.db.insert_multiple(anime_dict)
        self.db.close()
        avail_eps = database.fetch_available_episodes()
        self.assertEqual([{
            'name': 'test bangumi 3',
            'keyword': 'test bangumi 3',
            'translation_team': ['sumisora'],
            'ep': 7
        }, {
            'name': 'test bangumi 3',
            'keyword': 'test bangumi 3',
            'translation_team': ['sumisora'],
            'ep': 8
        }], avail_eps)

    def test_function_with_offset(self):
        """
        Test function if an offset anime is presented
        """
        anime_dict = [{
            'name': 'test bangumi 3',
            'keyword': 'test bangumi 3',
            'translation_team': ['sumisora'],
            'start_date': date.today() - timedelta(days=49),
            'dled_ep': 6,
            'total_ep': 13,
            'offset': 1
        }]
        self.db.insert_multiple(anime_dict)
        self.db.close()
        avail_eps = database.fetch_available_episodes()
        self.assertEqual([{
            'name': 'test bangumi 3',
            'keyword': 'test bangumi 3',
            'translation_team': ['sumisora'],
            'ep': 7
        }], avail_eps)


class UpdateAnimeInfoTests(unittest.TestCase):
    """
    Test cases to test update_anime_info
    """

    def setUp(self):
        """
        Configure database for test purposes. Remind to close db after data
        insertion.
        """
        database.DEFAULT_DATABASE = 'test.db'
        self.db = database.opendb()

    def tearDown(self):
        os.remove('test.db')

    def test_function_1(self):
        """
        Test function under situation with one entry in database
        """
        anime = {
            'name': 'test bangumi 2',
            'translation_team': ['sumisora'],
            'start_date': date.today() + timedelta(days=1),
            'dled_ep': 0,
            'total_ep': 12,
            'offset': 0
        }
        self.db.insert(anime)
        new_info = {
            'new_name': 'another',
            'new_translation_team': ['kmp'],
            'new_dled_ep': 2,
        }
        database.update_anime_info('test bangumi 2', new_info)
        q = tinydb.Query()
        new = self.db.get(q.name == 'another')
        self.assertEqual({
            'name': 'another',
            'translation_team': ['kmp'],
            'start_date': date.today() + timedelta(days=1),
            'dled_ep': 2,
            'total_ep': 12,
            'offset': 0
        }, new)
        self.db.close()


class RemoveAnimeTests(unittest.TestCase):
    """
    Test cases to test remove_anime
    """

    def setUp(self):
        """
        Configure database for test purposes. Remind to close db after data
        insertion.
        """
        database.DEFAULT_DATABASE = 'test.db'
        self.db = database.opendb()

    def tearDown(self):
        self.db.close()
        os.remove('test.db')

    def test_function_1(self):
        anime = {
            'name': 'test bangumi 2',
            'translation_team': ['sumisora'],
            'start_date': date.today() + timedelta(days=1),
            'dled_ep': 0,
            'total_ep': 12,
            'offset': 0
        }
        self.db.insert(anime)
        database.remove_anime('test bangumi 2')
        self.assertEqual(0, len(self.db.all()))
