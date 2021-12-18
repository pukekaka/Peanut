# -*- coding: utf-8 -*-
from typing import Dict
import pandas as pd

from utils import dict_to_html, dataframe_astype
from api.dart.corp_info.corp_profile import get_corp_profile as dart_get_corp_profile
from api.dart.shareholder.executive import get_executive_shareholder as dart_get_executive_shareholder
from api.dart.shareholder.majority import get_majority_shareholder as dart_get_majority_shareholder


class Corp(object):
    def __init__(self,
                 corp_code: str,
                 corp_name: str = None,
                 modify_date: str = None,
                 stock_code: str = None,
                 profile: bool = False):
        self._info = {
            'corp_code': corp_code,
            'corp_name': corp_name,
            'stock_code': stock_code,
            'modify_date': modify_date,
        }
        self._loading = False
        self._profile = profile

    def __getattr__(self, item):
        if item in self._info:
            return self._info[item]
        else:
            if self._profile is True:
                self.load()
            if item in self._info:
                return self._info[item]
            else:
                error = "'{} object has no attribute '{}".format(type(self).__name__, item)
                raise AttributeError(error)

    def __repr__(self) -> str:
        return '[{}] {}'.format(self.corp_code, self.corp_name)

    def __repr_html_(self) -> str:
        return dict_to_html(self.to_dict(), header=['Label' 'Data'])

    def load(self):
        if self._loading is False:
            info = dart_get_corp_profile(self._info['corp_code'])
            info.pop('status')
            info.pop('message')
            self._info.update(info)
            self._loading = True
        return self._info

    @property
    def info(self) -> Dict[str, str]:
        if self._profile is True:
            self.load()
        return self._info

    def update(self, info) -> Dict[str, str]:
        self._info.update(info)
        return self._info

    def to_dict(self) -> Dict[str, str]:
        return self.info

    def get_executive_shareholder(self):
        resp = dart_get_executive_shareholder(corp_code=self.corp_code)
        df = pd.DataFrame.from_dict(resp['list'])

        columns_astype = [
            ('sp_stock_lmp_cnt', int),
            ('sp_stock_lmp_irds_cnt', int),
            ('sp_stock_lmp_irds_rate', float),
            ('sp_stock_lmp_rate', float)
        ]

        df = dataframe_astype(df, columns_astype)
        return df

    def get_majority_shareholder(self):
        resp = dart_get_majority_shareholder(corp_code=self.corp_code)
        df = pd.DataFrame.from_dict(resp['list'])

        columns_astype = [
            ('stkqy', int),
            ('stkqy_irds', int),
            ('stkrt', float),
            ('stkrt_irds', float),
            ('ctr_stkqy', int),
            ('ctr_stkrt', float)
        ]

        df = dataframe_astype(df, columns_astype)
        return df
