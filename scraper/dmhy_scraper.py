"""Base class of scraper"""
import re

from bs4 import BeautifulSoup
import net

class DmhyScraper:
    """Scraper for dmhy"""

    def __init__(self):
        """Constructor"""
        self._base_url = 'http://share.dmhy.org'

    def _get_query_list(self, title, episode):
        """ Get query list of query with given title and episode

        returns:
        Text of query list page
        """
        query_url = self._base_url + '/topics/list'
        query_params = {
            'keyword': title + ' ' + _format_episode(episode)
        }

        return net.get(query_url, query_params)

    def _get_download_link(self, query_list, title, episode):
        """Parse query list page, then find the link of the download page of
        anime given title and episode.

        returns:
        Download link of anime given title and episode.
        If link cannot be found, None will be returned
        """
        parsed_query_list = BeautifulSoup(query_list, 'lxml')
        anime_table = parsed_query_list.find(id='topic_list')
        if anime_table is not None:
            anime_rows = _get_rows_of_table(anime_table)
            for row in anime_rows:
                entry_title_anchor = _get_a_tag_from_tr(row)
                entry_title = _get_text_in_a(entry_title_anchor)
                if title in entry_title and _format_episode(episode) in entry_title:
                    return self._get_url_from_href(entry_title_anchor['href'])

        return None

    def _get_url_from_href(self, href):
        """Get full url from href attribute of a tag.
        """
        full_url_pattern = re.compile(r'^http')
        if full_url_pattern.match(href) is None:
            # relative url
            return self._base_url + href
        else:
            # absolute url
            return href

    def find_download_page(self, *, title, episode):
        """Find correct download page based on params.

        Params are restricted to passing by name.

        returns:
        URL of download page
        """
        query_list = self._get_query_list(title, episode)
        return self._get_download_link(query_list, title, episode)

    def find_torrent_link(self, download_page):
        """Find torrent link from given download page

        returns:
        URL of torrent
        """
        parsed_download_page = BeautifulSoup(download_page, 'lxml')
        torrent_link_node = parsed_download_page.find(id='tabs-1')
        torrent_link = torrent_link_node.find('p').find('a')['href']
        return torrent_link

def _format_episode(episode):
    """Format Episode to 2 digits"""
    return '{:0>2}'.format(episode)

def _get_rows_of_table(table):
    """Get all rows of given table, excluding header."""
    return table.find_all('tr')[1:]

def _get_a_tag_from_tr(tr_tag):
    """Get a tag from given tr tag
    """
    return tr_tag.select('td.title > a')[0]

def _get_text_in_a(a_tag):
    """Get text in given a tag.
    """
    return ''.join(a_tag.strings).strip()
