"""
Parser for dmhy.org
"""
import bs4
import requests
from hanziconv import HanziConv


def get_download_url(name, ep, keyword, translation_team):
    """
    Search download url in dmhy.org
    """
    root_url = 'https://share.dmhy.org'
    payload = {'keyword': keyword + ' ' + '{:0>2}'.format(ep)}
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
        a = tr.select('td.title > a')[0]
        # Check the correctness of entry
        entry_desc = ''
        for string in a.strings:
            entry_desc += string
        print('Searching: {0}'.format(HanziConv.toSimplified(entry_desc)))
        if name in HanziConv.toSimplified(entry_desc):
            # Translation team check
            if (translation_team != []
                    and not any(trans_t in entry_desc for trans_t in translation_team)):
                continue
            download_page_url = a['href']
            print('download_page link:{0}'.format(download_page_url))
            download_page = requests.get(root_url + download_page_url)
            soup1 = bs4.BeautifulSoup(download_page.content, 'lxml')
            url_list = soup1.find(id='tabs-1')
            p = url_list.find('p')
            download_url = p.find('a')['href']
            break
    if download_url == '':
        raise FileNotFoundError
    return "https:" + download_url
