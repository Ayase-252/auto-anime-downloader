"""
Parser for dmhy.org
"""
import bs4
import requests
from hanziconv import HanziConv

import net


def get_download_url(name, ep, keyword, translation_team):
    """
    Search download url in dmhy.org
    """
    root_url = 'https://share.dmhy.org'
    payload = {'keyword': keyword + ' ' + '{:0>2}'.format(ep)}
    user_agent = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML,'
                      'like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    }
    print('DMHY scraper is searching for {} of {}'.format(ep, name))
    content = net.request_get_content(root_url + '/topics/list',
                                      retry=5,
                                      params=payload)
    soup = bs4.BeautifulSoup(content, 'lxml')
    trs = soup.find_all('tr')
    if len(trs) == 0:
        raise FileNotFoundError
    found_flag = False
    download_url = ''
    unified_name = name.lower()
    print('Unified name:{}'.format(unified_name))
    # Skip the table header
    for tr in trs[1:]:
        a = tr.select('td.title > a')[0]
        # Check the correctness of entry
        entry_desc = ''
        for string in a.strings:
            entry_desc += string
        # Eliminating spaces
        entry_desc = HanziConv.toSimplified(entry_desc.strip())
        try:
            print('Searching: {0}'.format(entry_desc))
        except:
            print('Experiencing encoding problem, but search is still going on.')
            print('Searching:', entry_desc.encode('utf-8'))
        unified_entry_desc = entry_desc.lower()
        if unified_name in unified_entry_desc:
            # Translation team check
            if (translation_team != []
                    and not any(trans_t.lower() in unified_entry_desc for trans_t in translation_team)):
                continue
            download_page_url = a['href']
            print('download_page link:{0}'.format(download_page_url))
            download_page_content = net.request_get_content(
                root_url + download_page_url,
                retry=5)
            soup1 = bs4.BeautifulSoup(download_page_content, 'lxml')
            url_list = soup1.find(id='tabs-1')
            p = url_list.find('p')
            download_url = p.find('a')['href']
            break
    if download_url == '':
        raise FileNotFoundError
    return "https:" + download_url
