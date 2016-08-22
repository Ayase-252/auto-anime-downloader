import unittest
import json
from datetime import date

import bangumi


class BangumiTestClass(unittest.TestCase):

    def test_parsed_json_to_dict_ascii(self):
        f = open(r'test/test-input-ascii.json', 'r', encoding='utf-8')
        test_str = f.read()
        f.close()
        parsed = json.loads(test_str, encoding='utf-8')
        pdict = bangumi.parsed_json_to_dict(parsed)
        self.assertEqual(pdict, {
            'name': 'Ano hi mita hana no namae wo bokutachi wa mada shiranai.',
            'keyword': 'Ano hi mita hana no namae wo bokutachi wa mada shiranai.',
            'start_date': date(2011, 4, 14),
            'translation_team': ['sumisora', 'emd'],
            'total_ep': 11,
            'dled_ep': 0,
            'offset': 0,
            'folder': 'Ano hi mita hana no namae wo bokutachi wa mada shiranai.'
        })

    def test_parsed_json_to_dict_ch(self):
        f = open(r'test/test-input-ch.json', 'r', encoding='utf-8')
        test_str = f.read()
        f.close()
        parsed = json.loads(test_str, encoding='utf-8')
        pdict = bangumi.parsed_json_to_dict(parsed)
        self.assertEqual(pdict, {
            'name': '少女与战车',
            'keyword': '少女与战车',
            'start_date': date(2012, 10, 8),
            'translation_team': ['测试字幕组'],
            'total_ep': 12,
            'dled_ep': 0,
            'offset': 0,
            'folder': '少女与战车'
        })
        f.close()

    def test_parsed_json_to_dict_jp(self):
        f = open(r'test/test-input-jp.json', 'r', encoding='utf-8')
        test_str = f.read()
        f.close()
        parsed = json.loads(test_str, encoding='utf-8')
        pdict = bangumi.parsed_json_to_dict(parsed)
        self.assertEqual(pdict, {
            'name': 'ふらいんうぃち',
            'keyword': 'ふらいんうぃち',
            'start_date': date(2016, 4, 9),
            'translation_team': [],
            'total_ep': 12,
            'dled_ep': 0,
            'offset': 0,
            'folder': 'ふらいんうぃち',
        })
        f.close()


class ParsedJSONToNewDictTests(unittest.TestCase):

    def test_function_1(self):
        new_dict = {
            'name': 'test_bangumi',
            'new_name': 'test bangumi 2',
            'new_translation_team': ['sumisora', 'emd'],
            'new_total_ep': '25',
            'new_dled_ep': '20',
            'new_start_date': '2016-05-05',
            'new_keyword': 'test',
            'new_offset': '2',
        }
        converted_dict = bangumi.parsed_json_to_new_dict(new_dict)
        self.assertEqual({
            'name': 'test_bangumi',
            'new_name': 'test bangumi 2',
            'new_translation_team': ['sumisora', 'emd'],
            'new_total_ep': 25,
            'new_dled_ep': 20,
            'new_start_date': date(2016, 5, 5),
            'new_keyword': 'test',
            'new_offset': 2
        }, converted_dict)
