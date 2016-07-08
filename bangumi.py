from datetime import datetime
import json


class Bangumi:

    def __init__(self, name, start_date, translation_team=[],
                 downloaded_ep=0, total_ep=99, offset=0):
        self.name = name
        self.start_date = start_date
        self.translation_team = translation_team
        self.downloaded_ep = downloaded_ep
        self.total_ep = total_ep
        self.offset = offset


def parse_from_json(json_str):
    bangumi = json.loads(json_str, encoding='utf-8')
    new_bangumi = {}
    new_bangumi['name'] = bangumi['name']
    new_bangumi['start_date'] = datetime.strptime(
        bangumi['start_date'], '%Y-%m-%d',).date()
    if 'translation_team' in bangumi:
        new_bangumi['translation_team'] = bangumi['translation_team']
    else:
        new_bangumi['translation_team'] = []
    if bangumi['total_ep'] is not None:
        new_bangumi['total_ep'] = int(bangumi['total_ep'])
    else:
        new_bangumi['total_ep'] = 99
    new_bangumi['downloaded_ep'] = 0
    new_bangumi['offset'] = 0
    return new_bangumi


def parsed_json_to_dict(parsed):
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
