import unittest
import os
from datetime import date, timedelta

import tinydb

import database


class DatabaseTests(unittest.TestCase):

    def setUp(self):
        """
        Configure database for test purposes. Remind to close db after data
        insertion.
        """
        database.DEFAULT_DATABASE = 'test.db'
        self.db = database.opendb()

    def tearDown(self):
        try:
            self.db.close()
        finally:
            os.remove('test.db')

    def test_fetch_available_episodes_normal_cond(self):
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
            'offset': 0,
            'folder': 'test bangumi 2'
        }, {
            'name': 'test bangumi 3',
            'keyword': 'test bangumi 3',
            'translation_team': ['sumisora'],
            'start_date': date.today() - timedelta(days=49),
            'dled_ep': 6,
            'total_ep': 13,
            'offset': 0,
            'folder': 'test bangumi 3'
        }
        ]
        self.db.insert_multiple(anime_dict)
        self.db.close()
        avail_eps = database.fetch_available_episodes()
        self.assertEqual([{
            'name': 'test bangumi 3',
            'keyword': 'test bangumi 3',
            'translation_team': ['sumisora'],
            'ep': 7,
            'folder': 'test bangumi 3'
        }, {
            'name': 'test bangumi 3',
            'keyword': 'test bangumi 3',
            'translation_team': ['sumisora'],
            'ep': 8,
            'folder': 'test bangumi 3'
        }], avail_eps)

    def test_fetch_available_episodes_offset_cond(self):
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
            'offset': 1,
            'folder': 'test bangumi 3'
        }]
        self.db.insert_multiple(anime_dict)
        self.db.close()
        avail_eps = database.fetch_available_episodes()
        self.assertEqual([{
            'name': 'test bangumi 3',
            'keyword': 'test bangumi 3',
            'translation_team': ['sumisora'],
            'ep': 7,
            'folder': 'test bangumi 3'
        }], avail_eps)

    def test_update_anime_info_normal_cond(self):
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
        self.db.close()
        self.assertEqual({
            'name': 'another',
            'translation_team': ['kmp'],
            'start_date': date.today() + timedelta(days=1),
            'dled_ep': 2,
            'total_ep': 12,
            'offset': 0
        }, new)

    def test_remove_anime_normal_cond(self):
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
        self.db.close()

    def test_remove_finished_anime(self):
        anime_group = [{
            'name': 'test bangumi 2',
            'translation_team': ['sumisora'],
            'start_date': date.today() + timedelta(days=1),
            'dled_ep': 12,
            'total_ep': 12,
            'offset': 0
        }, {
            'name': 'test bangumi 3',
            'translation_team': ['sumisora'],
            'start_date': date.today() + timedelta(days=1),
            'dled_ep': 11,
            'total_ep': 12,
            'offset': 0
        }]
        self.db.insert_multiple(anime_group)
        database.remove_finished_anime()
        self.assertEqual(1, len(self.db.all()))
        self.db.close()

    def test_get_anime_by_name(self):
        anime_group = [{
            'name': 'test bangumi 2',
            'translation_team': ['sumisora'],
            'start_date': date.today() + timedelta(days=1),
            'dled_ep': 12,
            'total_ep': 12,
            'offset': 0
        }, {
            'name': 'test bangumi 3',
            'translation_team': ['sumisora'],
            'start_date': date.today() + timedelta(days=1),
            'dled_ep': 11,
            'total_ep': 12,
            'offset': 0
        }]
        self.db.insert_multiple(anime_group)
        r = database.get_anime_by_name('test bangumi 2')
        self.assertEqual({
            'name': 'test bangumi 2',
            'translation_team': ['sumisora'],
            'start_date': date.today() + timedelta(days=1),
            'dled_ep': 12,
            'total_ep': 12,
            'offset': 0
        }, r)

    def test_get_all_anime(self):
        anime_group = [{
            'name': 'test bangumi 2',
            'translation_team': ['sumisora'],
            'start_date': date.today() + timedelta(days=1),
            'dled_ep': 12,
            'total_ep': 12,
            'offset': 0
        }, {
            'name': 'test bangumi 3',
            'translation_team': ['sumisora'],
            'start_date': date.today() + timedelta(days=1),
            'dled_ep': 11,
            'total_ep': 12,
            'offset': 0
        }]
        self.db.insert_multiple(anime_group)
        r = database.get_all_anime()
        self.assertEqual(2, len(r))
