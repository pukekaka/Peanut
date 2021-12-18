# -*- coding: utf-8 -*-
import re
from typing import Union, List

from utils import Singleton
from utils import Spinner
from service.info.corp import Corp

from crawler.krx.corp_list import get_corp_list as krx_get_corp_list
from api.dart.corp_info.corp_code import get_corp_code as dart_get_corp_code


def get_corp_list():
    return CorpList()


def market_type_checker(market: Union[str, list]) -> List[str]:
    if isinstance(market, str):
        market = [x for x in market]
    market = [x.upper() for x in market]

    for m in market:
        if m not in ['Y', 'K', 'N', 'E']:
            raise ValueError('Invalid market type')
    return market


class CorpList(object, metaclass=Singleton):
    def __init__(self, profile=False):
        self._corps = None
        self._corp_codes = dict()
        self._corp_names = []
        self._corp_cls_list = []
        self._corp_product = []
        self._corp_sector = []
        self._sectors = []

        self._stock_codes = dict()
        self._del_listing = dict()
        self._stock_market = dict()
        self._profile = profile

        self.load(profile=self._profile)

    def load(self, profile=False):
        if self._corps is None:
            self._load(profile=profile)

    def _load(self, profile=False):
        spinner = Spinner('[KRX] Loading Company List')
        spinner.start()
        for k in ['Y', 'K', 'N']:
            data = krx_get_corp_list(k, False)
            self._stock_market = {**self._stock_market, **data}

        spinner.succeed()
        spinner.stop()

        spinner = Spinner('[DART] Loading Company Code')
        spinner.start()

        sectors = set()

        self._corps = [Corp(**x, profile=profile) for x in dart_get_corp_code()]
        for idx, x in enumerate(self._corps):
            self._corp_codes[x.corp_code] = idx
            self._corp_names.append(x.corp_name)
            stock_code = x.stock_code
            # Market type check
            corp_cls = 'E'
            product = None
            sector = None
            if stock_code is not None:
                try:
                    info = self._stock_market[stock_code]
                    corp_cls = info['corp_cls']
                    product = info['product']
                    sector = info['sector']
                    sectors.add(sector)
                    self._stock_codes[stock_code] = idx
                    # Update information
                    x.update(info)
                except KeyError:
                    self._del_listing[stock_code] = idx
                    pass
            self._corp_cls_list.append(corp_cls)
            self._corp_product.append(product)
            self._corp_sector.append(sector)
        self._sectors = sorted(list(sectors))

        spinner.succeed()
        spinner.stop()

    @property
    def corps(self):
        self.load(profile=self._profile)
        return self._corps

    def find_by_corp_code(self, corp_code):
        corps = self.corps
        idx = self._corp_codes.get(corp_code)
        return corps[idx] if idx is not None else None

    def find_by_corp_name(self, corp_name, exactly=False, market='YKNE'):
        corps = self.corps
        res = []
        if exactly is True:
            corp_name = '^' + corp_name + '$'
        regex = re.compile(corp_name)

        market = market_type_checker(market)

        for idx, corp_name in enumerate(self._corp_names):
            if regex.search(corp_name) is not None:
                if self._corp_cls_list[idx] in market:
                    res.append(corps[idx])

        return res if len(res) > 0 else None

    def find_by_product(self, product, market='YKN'):
        corps = self.corps
        res = []

        regex = re.compile(product)

        market = market_type_checker(market)
        if 'E' in market:
            raise ValueError('ETC Market is not supported')

        for idx, product in enumerate(self._corp_product):
            if product and regex.search(product) is not None:
                if self._corp_cls_list[idx] in market:
                    res.append(corps[idx])
        return res if len(res) > 0 else None

    def find_by_sector(self, sector, market='YKN'):
        corps = self.corps
        res = []

        regex = re.compile(sector)

        market = market_type_checker(market)
        if 'E' in market:
            raise ValueError('ETC Market is not supported')

        for idx, sector in enumerate(self._corp_sector):
            if sector and regex.search(sector) is not None:
                if self._corp_cls_list[idx] in market:
                    res.append(corps[idx])
        return res if len(res) > 0 else None

    @property
    def sectors(self):
        return self._sectors

    def find_by_stock_code(self, stock_code, include_del_listing=False):
        corps = self.corps
        idx = self._stock_codes.get(stock_code)
        if include_del_listing and idx is None:
            idx = self._del_listing.get(stock_code)
        return corps[idx] if idx is not None else None

    def __repr__(self):
        corps = self.corps
        return 'Number of companies: {}'.format(len(corps))

    def __getitem__(self, item):
        corps = self.corps
        return corps[item]

    def __len__(self):
        corps = self.corps
        return len(corps)
