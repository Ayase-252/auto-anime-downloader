import unittest
import os
from datetime import date

import tinydb

import main
import database


class MainTests(unittest.TestCase):

    def setUp(self):
        database.DEFAULT_DATABASE = 'test.db'
        self.db = database.opendb()

    def tearDown(self):
        self.db.close()
        os.remove('test.db')

    def test_update(self):
        anime = {
            'name': 'test_bangumi_1',
            'start_date': date.today()
        }
        self.db.insert(anime)
        main.update('test/test-main-update.json')
        q = tinydb.Query()
        r = self.db.get(q.name == 'new name')
        self.assertEqual({
            'name': 'new name',
            'keyword': 'new',
            'start_date': date(2016, 1, 1),
            'translation_team': ['sumisora'],
            'dled_ep': 1,
            'total_ep': 12,
            'offset': 1
        }, r)

    def test_add(self):
        main.add('test/test-main-add.json')
        q = tinydb.Query()
        r = self.db.get(q.name == 'Ano hi mita hana no namae wo bokutachi wa '
                                  'mada shiranai.')
        self.assertEqual({
            'name': 'Ano hi mita hana no namae wo bokutachi wa mada shiranai.',
            'start_date': date(2011, 4, 14),
            'translation_team': ['sumisora', 'emd'],
            'total_ep': 11,
            'dled_ep': 0,
            'keyword': 'Ano hi mita hana no namae wo bokutachi wa '
                       'mada shiranai.',
            'offset': 0,
            'folder': 'Ano hi mita hana no namae wo bokutachi wa '
                       'mada shiranai.'
        }, r)
