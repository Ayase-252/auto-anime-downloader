"""
Parser for dmhy.org
"""
import bs4
import requests

from filemeta import FileMeta


def get_download_url(file_meta):
    """
    Search download url in dmhy.org
    """
    root_url = 'https://share.dmhy.org'
    payload = {'keyword': file_meta.name + ' ' + '{:0>2}'.format(file_meta.ep)}
    search = requests.get(root_url + '/topics/list', params=payload)
    soup = bs4.BeautifulSoup(search.content, 'lxml')
    print('search url:{0}'.format(search.url))
    trs = soup.find_all('tr')
    if len(trs) == 0:
        raise FileNotFoundError
    found_flag = False
    download_url = ''
    # Skip the table header
    for tr in trs[1:]:
        a = tr.select('td.title > a')
        download_page_url = a[0]['href']
        print('download_page link:{0}'.format(download_page_url))
        download_page = requests.get(root_url + download_page_url)
        soup1 = bs4.BeautifulSoup(download_page.content, 'lxml')
        url_list = soup1.find(id='tabs-1')
        p = url_list.find('p')
        download_url = p.find('a')['href']
        break
    return "https:" + download_url
