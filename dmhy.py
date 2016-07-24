"""
Parser for dmhy.org
"""
import bs4
import requests
from hanziconv import HanziConv


def get_download_uri(name, ep, keyword, translation_team):
    """
    Search download uri in dmhy.org
    """
    root_uri = 'https://share.dmhy.org'
    payload = {'keyword': keyword + ' ' + '{:0>2}'.format(ep)}
    user_agent = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML,'
                      'like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    }
    search = requests.get(root_uri + '/topics/list',
                          headers=user_agent,
                          params=payload,
                          timeout=5)
    soup = bs4.BeautifulSoup(search.content, 'lxml')
    print('search uri:{0}'.format(search.uri))
    trs = soup.find_all('tr')
    if len(trs) == 0:
        raise FileNotFoundError
    found_flag = False
    download_uri = ''
    # Skip the table header
    for tr in trs[1:]:
        a = tr.select('td.title > a')[0]
        # Check the correctness of entry
        entry_desc = ''
        for string in a.strings:
            entry_desc += string
        # Eliminating spaces
        entry_desc = HanziConv.toSimplified(entry_desc.strip())
        print('Searching: {0}'.format(entry_desc))
        unified_name = name.lower()
        unified_entry_desc = entry_desc.lower()
        print('Unified name:{}'.format(unified_name))
        if unified_name in unified_entry_desc:
            # Translation team check
            if (translation_team != []
                    and not any(trans_t.lower() in unified_entry_desc for trans_t in translation_team)):
                continue
            download_page_uri = a['href']
            print('download_page link:{0}'.format(download_page_uri))
            download_page = requests.get(root_uri + download_page_uri,
                                         headers=user_agent,
                                         timeout=5)
            soup1 = bs4.BeautifulSoup(download_page.content, 'lxml')
            uri_list = soup1.find(id='tabs-1')
            p = uri_list.find('p')
            download_uri = p.find('a')['href']
            break
    if download_uri == '':
        raise FileNotFoundError
    return "https:" + download_uri
