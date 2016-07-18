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
        db = database.opendb()
        bangumi_dict = [
            {
                'name': 'test bangumi 2',
                'translation_team': ['sumisora'],
                'start_date': date.today() + timedelta(days=1),
                'next_onair_date': date.today() + timedelta(days=1),
                'dled_ep': 0,
                'total_ep': 12,
                'offset': 0
            }, {
                'name': 'test bangumi 3',
                'translation_team': ['sumisora'],
                'start_date': date.today() - timedelta(days=49),
                'next_onair_date': date.today(),
                'dled_ep': 6,
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
        intended_episodes = [FileMeta('test bangumi 3', 7, ['sumisora'])]
        self.assertEqual(intended_episodes, unloaded_episodes)

    def test_unloaded_episode_2(self):
        """
        Test the function of unloaded episode.

        Test case is adapted from a bug happened in early stage of development.
        """
        database.DEFAULT_DATABASE = 'test_unloaded_episode_2'
        db = database.opendb()
        bangumi = {
            'name': 'test bangumi temp',
            'translation_team': [],
            'start_date': date.today() - timedelta(days=1),
            'next_onair_date': date.today() - timedelta(days=1),
            'dled_ep': 0,
            'total_ep': 1,
            'offset': 0
        }
        db.insert(bangumi)
        db.close()
        unloaded_episodes = database.unloaded_episodes()
        os.remove('test_unloaded_episode_2')
        intended_episodes = [FileMeta('test bangumi temp', 1, [])]
        self.assertEqual(intended_episodes, unloaded_episodes)
