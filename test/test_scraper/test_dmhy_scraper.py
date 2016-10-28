"""Unit tests of dmhy scraper"""
import unittest
import re

from bs4 import BeautifulSoup
import requests_mock

from scraper.dmhy_scraper import DmhyScraper
import net

class DmhyScraperTestClass(unittest.TestCase):
    """Test class of Dmhy Scraper"""

    def verify_download_page(self, download_page, title, episode):
        """Verify the correctness of download page
        """
        parsed_html = BeautifulSoup(download_page, 'lxml')
        self.assertNotEqual(len(parsed_html.find(text=re.compile(title))), 0)
        self.assertNotEqual(len(parsed_html.find(
            text=re.compile('{0}|{0:0>2}|第{0}话|第{0}集'.format(episode)))), 0)

    @requests_mock.Mocker()
    def test_normal_scrape(self, mocker):
        """Test scraper in normal condition"""
        # Set mock
        mock_query_list = open(
            'test/test_scraper/gn_query_list.html', encoding='utf-8')
        mock_download_page = open(
            'test/test_scraper/gn_01_download_page.html', encoding='utf-8')
        mocker.get('http://share.dmhy.org/topics/list?keyword=少女编号+01',
                   text=mock_query_list.read())
        mocker.get('http://share.dmhy.org/topics/view/444596_Girlish_Number_01_GB_720P.html',
                   text=mock_download_page.read())
        mock_query_list.close()
        mock_download_page.close()

        scraper = DmhyScraper()
        title = '少女编号'
        episode = 1
        download_page_url = scraper.find_download_page(title=title,
                                                       episode=episode)
        self.assertIsNotNone(download_page_url)
        download_page = net.get(download_page_url)
        self.assertIsNotNone(download_page)
        self.verify_download_page(download_page, title, episode)

    @requests_mock.Mocker()
    def test_scrape_anime_not_exist(self, mocker):
        """Test scraper in condition that given anime is fictional."""
        mock_query_list = open(
            'test/test_scraper/empty_query_list.html', encoding='utf-8')
        mocker.get('http://share.dmhy.org/topics/list?keyword=Anime+not+exist+100',
            text=mock_query_list.read())
        mock_query_list.close()

        scraper = DmhyScraper()
        download_page_url = scraper.find_download_page(title='Anime not exist',
                                                       episode=100)
        self.assertIsNone(download_page_url)

    def test_scrape_torrent_from_download_page(self):
        """Test function to scraper torrent link from a sample download page.
        """
        scraper = DmhyScraper()
        test_download_page_file = open(
            'test/test_scraper/dmhy_test_download_page.html', encoding='utf-8')
        test_download_page = test_download_page_file.read()
        test_download_page_file.close()

        torrent_link = scraper.find_torrent_link(test_download_page)
        self.assertEqual(
            torrent_link,
            'http://dl.dmhy.org/2016/10/28/5c9f228b7bf0cf7dbb310e457a94b3534c63ed5d.torrent')
