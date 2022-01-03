# -*- coding: utf-8 -*-
import re
import copy

from urllib.parse import parse_qs

from bs4 import BeautifulSoup

from service.dart.info.search.pages import Page
from utils import request

class Report(object):
    _DART_URL_ = 'https://dart.fss.or.kr'
    _REPORT_URL_ = _DART_URL_ + '/dsaf001/main.do'
    _DOWNLOAD_URL_ = _DART_URL_ + '/pdf/download/main.do'

    def __init__(self, **kwargs):
        self.rcp_no = kwargs.get('rcp_no')
        if self.rcp_no is None:
            self.rcept_no = kwargs.get('rcept_no')
            kwargs.pop('rcept_no')
        else:
            kwargs.pop('rcp_no')

        if self.rcp_no is None:
            raise ValueError('rcp_no must be not None')

        self.dcm_no = kwargs.get('dcm_no')
        self.info = copy.deepcopy(kwargs)
        if self.dcm_no:
            self.info.pop('dcm_no')

        self.html = None
        self._pages = None
        self._xbrl = None
        self._related_reports = None
        self._attached_files = None
        self._attached_reports = None

        lazy_loading = kwargs.get('lazy_loading', True)
        if not lazy_loading:
            self.load()

    @property
    def rcept_no(self):
        return self.rcp_no

    @rcept_no.setter
    def rcept_no(self, rcept_no):
        self.rcp_no = rcept_no

    def __getattr__(self, item):
        if item in self.info:
            return self.info[item]
        else:
            error = "'{}' object has no attribute '{}'".format(type(self).__name__, item)
            raise AttributeError(error)

    def _get_report(self):
        payload = dict(rcpNo=self.rcp_no)
        if self.dcm_no:
            payload['dcmNo'] = self.dcm_no
        resp = request.get(url=self._REPORT_URL_, referer=self._DART_URL_)
        self.html = BeautifulSoup(resp.text, 'html.parser')
