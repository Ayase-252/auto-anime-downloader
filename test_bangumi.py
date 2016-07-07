import unittest
from datetime import date

import bangumi


class BangumiTestClass(unittest.TestCase):

    def test_parse_from_json_ascii(self):
        f = open(r'test-input-ascii.json', 'r', encoding='utf-8')
        test_str = f.read()
        parsed = bangumi.parse_from_json(test_str)
        self.assertEqual(parsed, {
            'name': 'Ano hi mita hana no namae wo bokutachi wa mada shiranai.',
            'start_date': date(2011, 4, 14),
            'translation_team': ['sumisora', 'emd'],
            'total_ep': 11,
            'downloaded_ep': 0,
            'offset': 0
        })
        f.close()

    def test_parse_from_json_ch(self):
        f = open(r'test-input-ch.json', 'r', encoding='utf-8')
        test_str = f.read()
        parsed = bangumi.parse_from_json(test_str)
        self.assertEqual(parsed, {
            'name': '少女与战车',
            'start_date': date(2012, 10, 8),
            'translation_team': ['测试字幕组'],
            'total_ep': 12,
            'downloaded_ep': 0,
            'offset': 0
        })
        f.close()

    def test_parse_from_json_jp(self):
        f = open(r'test-input-jp.json', 'r', encoding='utf-8')
        test_str = f.read()
        parsed = bangumi.parse_from_json(test_str)
        self.assertEqual(parsed, {
            'name': 'ふらいんうぃち',
            'start_date': date(2016, 4, 9),
            'translation_team': [],
            'total_ep': 12,
            'downloaded_ep': 0,
            'offset': 0
        })
        f.close()
