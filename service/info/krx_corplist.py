# -*- coding: utf-8 -*-

from utils import Singleton
from utils import Spinner
from crawler.krx.corplist import get_stock_market_list


def get_corp_list():
    return CorpList()


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
        spinner = Spinner('Loading Stock Market Information (KRX)')
        spinner.start()
        for k in ['Y', 'K', 'N']:
            data = get_stock_market_list(k, False)
            self._stock_market = {**self._stock_market, **data}

        if data is not None:
            spinner.succeed()
        else :
            spinner.fail()

        spinner.stop()

