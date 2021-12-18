# -*- coding: utf-8 -*-
from utils import request
from bs4 import BeautifulSoup


def get_corp_list(corp_cls: str, include_corp_name=True) -> dict:
    if corp_cls.upper() == 'E':
        raise ValueError('ETC market is not supported')

    corp_cls_to_market = {
        "Y": "stockMkt",
        "K": "kosdaqMkt",
        "N": "konexMkt",
    }

    url = 'http://kind.krx.co.kr/corpgeneral/corpList.do'
    referer = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=loadInitPage'

    market_type = corp_cls_to_market[corp_cls.upper()]
    payload = {
        'method': 'download',
        'pageIndex': 1,
        'currentPageSize': 5000,
        'orderMode': 3,
        'orderStat': 'D',
        'searchType': 13,
        'marketType': market_type,
        'fiscalYearEnd': 'all',
        'location': 'all',
    }

    corp_list = dict()

    resp = request.post(url=url, payload=payload, referer=referer)
    html = BeautifulSoup(resp.text, 'html.parser')
    rows = html.find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 0:
            corp_name = cols[0].text.strip()
            stock_code = cols[1].text.strip()
            sector = cols[2].text.strip()
            product = cols[3].text.strip()
            corp_info = {'sector': sector, 'product': product, 'corp_cls': corp_cls}
            if include_corp_name:
                corp_info['corp_name'] = corp_name
            corp_list[stock_code] = corp_info

    return corp_list
