"""Base class of scraper"""
import requests
from bs4 import BeautifulSoup


class DmhyScraper:
    """Scraper for dmhy"""

    def __init__(self):
        """Constructor"""
        self._base_url = 'https://share.dmhy.org'

    def find_download_page(self, *, title, episode):
        """Find correct download page based on params.

        Params are restricted to passing by name.

        return:
        URL of download page
        """
        params = {'keyword': title + ' ' + _format_episode(episode)}
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKi'
            't/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        query_list = requests.get(
            self._base_url + '/topics/list', params=params, headers=headers)
        print(query_list.url)
        parsed_query_list = BeautifulSoup(query_list.text, 'lxml')

        anime_entries = parsed_query_list.find_all(
            'tr')[1:]  # skip the header of table
        for entry in anime_entries:
            entry_title_anchor = entry.select('td.title > a')[0]
            entry_title = ''
            for strip in entry_title_anchor.strings:
                entry_title += strip
            entry_title = entry_title.strip()
            print(entry_title)
            if title in entry_title and _format_episode(episode) in entry_title:
                return self._base_url+entry_title_anchor['href']

        return None

def _format_episode(episode):
    """Format Episode to 2 digits"""
    return '{:0>2}'.format(episode)
