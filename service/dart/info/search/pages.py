# -*- coding: utf-8 -*-

import re
import base64

from typing import Dict
from bs4 import BeautifulSoup
from utils import request


class Page(object):
    _BASE_URL_ = 'https://dart.fss.or.kr/report/viewer.do'

    def __init__(self,
                 title: str,
                 rcp_no: str,
                 dcm_no: str,
                 ele_id: int,
                 offset: str,
                 length: str,
                 dtd: str,
                 lazy_loading=True):
        self.title = title
        self.rcp_no = rcp_no
        self.dcm_no = dcm_no
        self.ele_id = ele_id
        self._offset = offset
        self._length = length
        self._dtd = dtd
        self._html = None
        if not lazy_loading:
            self.load()

    @property
    def html(self):
        if self._html is None:
            self.load()
        return self._html

    def load(self):
        def change_url(bs, tag):
            tags = bs.find_all(attrs={tag: re.compile(r'.*')})
            if tags:
                for t in tags:
                    t[tag] = "https://dart.fss.or.kr" + t[tag]
            return bs

        def add_prefix(match_obj):
            return r"window.open('https://dart.fss.or.kr" + match_obj.group(1) + r"'"

        payload = {
            'rcpNo': self.rcp_no,
            'dcmNo': self.dcm_no,
            'eleId': self.ele_id,
            'offset': self._offset,
            'length': self._length,
            'dtd': self._dtd
        }
        html = request.get(url=self._BASE_URL_, payload=payload,referer=self._BASE_URL_).content

        try:
            html = html.decode()
        except UnicodeDecodeError:
            html = html.decode('cp949')
        finally:
            soup = BeautifulSoup(html, 'html.parser')
            meta = soup.find('meta', {'content': re.compile(r'charset')})
            if meta:
                meta['content'] = meta['content'].replace('euc-kr', 'utf-8')

            soup = change_url(soup, 'href')
            soup = change_url(soup, 'src')

            html = str(soup)
            html = re.sub(r'window.open\(\'(.*?)\'', add_prefix, html)

            self._html = html

    def to_dict(self, summary=True) -> Dict[str, str]:
        info = dict()
        info['title'] = self.title
        info['ele_id'] = self.ele_id
        if not summary:
            info['rcp_no'] = self.rcp_no
            info['dcm_no'] = self.dcm_no
            info['offset'] = self._offset
            info['length'] = self._length
            info['dtd'] = self._dtd
        return info

    def __repr__(self) -> str:
        from pprint import pformat
        return pformat(self.to_dict(summary=False))

    def _repr_html(self) -> str:
        if self.html is None:
            self.load()
        if len(self.html) == 0:
            html = 'blank page'
        else:
            html = self.html
        base64_html = base64.b64encode(bytes(html, 'utf-8')).decode('utf-8')
        return r'<iframe src="data:text/html;base64,' + base64_html + r'" style="width:100%; height:500px;"></iframe>'

    def __str__(self) -> str:
        from pprint import pformat
        return pformat(self.to_dict())
