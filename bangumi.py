"""
Bangumi module
"""

from datetime import datetime
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
    new_bangumi['downloaded_ep'] = 0
    new_bangumi['offset'] = 0
    return new_bangumi


def read_bangumi_from_file(filepath):
    """
    Read bangumi infomation from file, file should be writen in JSON format

    param:
    filepath        path of file providing bangumi info
    """
    f = open(filepath, 'r', encoding='utf-8')
    parsed = json.loads(f.read(), encoding='utf-8')
    f.close()
    bangumi_list = []
    for bangumi in parsed:
        new_bangumi = parsed_json_to_dict(bangumi)
        bangumi_list.append(new_bangumi)
    return bangumi_list
