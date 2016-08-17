"""
Plugins of Management System
"""
import json
from datetime import datetime

from manage_base import ManagePluginBase
from bangumi import get_default_dict


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
