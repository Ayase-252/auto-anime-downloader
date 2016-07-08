import unittest
import json
from datetime import date

import bangumi


class BangumiTestClass(unittest.TestCase):

    def test_parsed_json_to_dict_ascii(self):
        f = open(r'test-input-ascii.json', 'r', encoding='utf-8')
        test_str = f.read()
        f.close()
        parsed = json.loads(test_str, encoding='utf-8')
        pdict = bangumi.parsed_json_to_dict(parsed)
        self.assertEqual(pdict, {
            'name': 'Ano hi mita hana no namae wo bokutachi wa mada shiranai.',
            'start_date': date(2011, 4, 14),
            'translation_team': ['sumisora', 'emd'],
            'total_ep': 11,
            'downloaded_ep': 0,
            'offset': 0
        })

    def test_parsed_json_to_dict_ch(self):
        f = open(r'test-input-ch.json', 'r', encoding='utf-8')
        test_str = f.read()
        f.close()
        parsed = json.loads(test_str, encoding='utf-8')
        pdict = bangumi.parsed_json_to_dict(parsed)
        self.assertEqual(pdict, {
            'name': '少女与战车',
            'start_date': date(2012, 10, 8),
            'translation_team': ['测试字幕组'],
            'total_ep': 12,
            'downloaded_ep': 0,
            'offset': 0
        })
        f.close()

    def test_parsed_json_to_dict_jp(self):
        f = open(r'test-input-jp.json', 'r', encoding='utf-8')
        test_str = f.read()
        f.close()
        parsed = json.loads(test_str, encoding='utf-8')
        pdict = bangumi.parsed_json_to_dict(parsed)
        self.assertEqual(pdict, {
            'name': 'ふらいんうぃち',
            'start_date': date(2016, 4, 9),
            'translation_team': [],
            'total_ep': 12,
            'downloaded_ep': 0,
            'offset': 0
        })
        f.close()

    def test_read_bangumi_from_file(self):
        read_list = bangumi.read_bangumi_from_file('test-input.json')
        self.assertEqual(read_list, [{
            'name': 'Ano hi mita hana no namae wo bokutachi wa mada shiranai.',
            'start_date': date(2011, 4, 14),
            'translation_team': ['sumisora', 'emd'],
            'total_ep': 11,
            'downloaded_ep': 0,
            'offset': 0
        }, {
            'name': 'ふらいんうぃち',
            'start_date': date(2016, 4, 9),
            'translation_team': [],
            'total_ep': 12,
            'downloaded_ep': 0,
            'offset': 0
        }, {
            'name': '少女与战车',
            'start_date': date(2012, 10, 8),
            'translation_team': [],
            'total_ep': 99,
            'downloaded_ep': 0,
            'offset': 0
        }
        ])
