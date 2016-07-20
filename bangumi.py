"""
Bangumi module
"""

from datetime import datetime, timedelta
import json


def parsed_json_to_dict(parsed):
    """
    Convert parsed dict into dict with python built-in type

    param:
    parsed      parsed dict by json decoder
    """
    new_bangumi = {}
    new_bangumi['name'] = parsed['name']
    new_bangumi['start_date'] = datetime.strptime(
        parsed['start_date'], '%Y-%m-%d').date()
    if 'translation_team' in parsed:
        new_bangumi['translation_team'] = parsed['translation_team']
    else:
        new_bangumi['translation_team'] = []
    if 'total_ep' in parsed:
        new_bangumi['total_ep'] = int(parsed['total_ep'])
    else:
        new_bangumi['total_ep'] = 99
    if 'dled_ep' in parsed:
        new_bangumi['dled_ep'] = int(parsed['dled_ep'])
    else:
        new_bangumi['dled_ep'] = 0
    if 'keyword' in parsed:
        new_bangumi['keyword'] = parsed['keyword']
    else:
        new_bangumi['keyword'] = new_bangumi['name']
    new_bangumi['offset'] = 0
    return new_bangumi


def parsed_json_to_new_dict(parsed):
    """
    Convert parsed dict into dict with python built-in type used by update
    function

    params:
    parsed:     parsed dict by json decode
    """
    new_anime = {}
    new_anime['name'] = parsed['name']
    for key in parsed:
        if key.startswith('new_'):
            if key[4:] in ['translation_team', 'keyword', 'name']:
                new_anime[key] = parsed[key]
            elif key[4:] in ['total_ep', 'dled_ep', 'offset']:
                new_anime[key] = int(parsed[key])
            elif key[4:] in ['start_date']:
                new_anime[key] = datetime.strptime(
                    parsed[key], '%Y-%m-%d').date()
    return new_anime


def read_bangumi_from_file(filepath):
    """
    Read bangumi infomation from file, file should be writen in JSON format

    param:
    filepath        path of file providing bangumi info
    """
    print('Reading from file {0}'.format(filepath))
    f = open(filepath, 'r', encoding='utf-8')
    parsed = json.loads(f.read(), encoding='utf-8')
    f.close()
    bangumi_list = []
    for bangumi in parsed:
        new_bangumi = parsed_json_to_dict(bangumi)
        bangumi_list.append(new_bangumi)
    return bangumi_list
