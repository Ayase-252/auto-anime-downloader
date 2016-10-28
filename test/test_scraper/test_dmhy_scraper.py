import unittest
import re
import requests
from bs4 import BeautifulSoup
from scraper.dmhy_scraper import DmhyScraper
from test.configure import *


class DmhyScraperTestClass(unittest.TestCase):

    #@unittest.skipUnless(CONNECT_TO_INTERNET, 'not connect to internet')
    def test_normal_scrape(self):
        scraper = DmhyScraper()
        download_page_url = scraper.find_download_page(title='少女编号',
                                                       episode=1)
        self.assertIsNotNone(download_page_url)
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKi'
            't/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        download_page = requests.get(download_page_url, headers=headers)
        self.assertEqual(download_page.status_code, 200)
        parsed_html = BeautifulSoup(download_page.text, 'lxml')
        self.assertNotEqual(len(parsed_html.find(text=re.compile('少女编号'))), 0)
        self.assertNotEqual(len(parsed_html.find(
            text=re.compile('1|01|第1话|第1集'))), 0)
