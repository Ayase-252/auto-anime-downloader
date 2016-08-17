"""
Plugins of Management System
"""
import json
from datetime import datetime

from manage_base import ManagePluginBase
from bangumi import get_default_dict
from database import get_all_anime


class Add(ManagePluginBase):
    """
    Add entries to database.

    The function generates an empty JSON file containing default value. Fill
    it. Then, invoke aad add file_path to add enties to database.
    """
    description = 'Generate a standard empty JSON file.'

    @classmethod
    def func(cls):
        """
        Generate a JSON file containing num empty enties

        user input:
        num     Number of enties
        """
        num = int(input('Number of anime you want to add: '))
        default_dict = get_default_dict()
        default_arr = [default_dict for _ in range(num)]
        json_str = json.dumps(default_arr, indent=4, separators=(',', ':'))
        generate_file = open('new_bangumi_'
                             + datetime.now().strftime('%Y-%m-%d-%H%M%S')
                             + '.json', 'w')
        generate_file.write(json_str)
        generate_file.close()
        print('File has been generated.')


class Change(ManagePluginBase):
    """
    Change entries in database.

    The function generates a JSON file compatable with change rule based on
    designated entries.
    """
    description = 'Generate a standard file containing entries you intent to change'

    @classmethod
    def func(cls):
        anime = get_all_anime()
        for key, entry in enumerate(anime):
            print('Number', key)
            print(entry)
            print('')
        user_input = input(
            'Input numbers of anime you want to change(Seperate by space): ')
        choices = user_input.split(' ')
        choices = [int(i) for i in choices]
        change_list = [anime[choice] for choice in choices]
        new_change_list = []
        for entry in change_list:
            new_entry = {'name': entry['name']}
            for key, value in entry.items():
                new_entry['new_' + key] = value
            new_entry['new_start_date'] = new_entry[
                'new_start_date'].strftime('%Y-%m-%d')
            new_change_list.append(new_entry)
        generate_file = open('change_anime_'
                             + datetime.now().strftime('%Y-%m-%d-%H%M%S')
                             + '.json', 'w')
        json.dump(new_change_list, generate_file,
                  indent=4, separators=(',', ':'), ensure_ascii=False)
        generate_file.close()
        print('File has been generated.')
