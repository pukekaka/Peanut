# -*- coding: utf-8 -*-
from typing import Dict, Union, List
import pandas as pd

from utils import dict_to_html, dataframe_astype
from api.dart.corp_info.company import get_corp_info as dart_get_corp_info

from api.dart.shareholder.elestock import get_executive_shareholder as dart_get_executive_shareholder
from api.dart.shareholder.majorstock import get_majority_shareholder as dart_get_majority_shareholder


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
            info = dart_get_corp_info(self._info['corp_code'])
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

    # def search(self,
    #            bgn_de: str = None,
    #            end_de: str = None,
    #            last_reprt_at: str = 'N',
    #            pblntf_ty: Union[str, List[str], None] = None,
    #            pblntf_detail_ty: Union[str, List[str], None] = None,
    #            corp_cls: str = None,
    #            sort: str = 'date',
    #            sort_mth: str = 'desc',
    #            page_no: int = 1,
    #            page_count: int = 10):
    #
    #     return dart_search(self.corp_code, bgn_de=bgn_de, end_de=end_de, last_reprt_at=last_reprt_at, pblntf_ty=pblntf_ty, pblntf_detail_ty=pblntf_detail_ty, corp_cls=corp_cls, sort=sort, sort_mth=sort_mth, page_no=page_no, page_count=page_count)
    #
