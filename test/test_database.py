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
            'translation_team': ['sumisora'],
            'start_date': date.today() + timedelta(days=1),
            'dled_ep': 0,
            'total_ep': 12,
            'offset': 0
        }, {
            'name': 'test bangumi 3',
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
            'translation_team': ['sumisora'],
            'ep': 7
        }, {
            'name': 'test bangumi 3',
            'translation_team': ['sumisora'],
            'ep': 8
        }], avail_eps)
