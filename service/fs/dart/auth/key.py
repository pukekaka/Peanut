# -*- coding: utf-8 -*-
from utils import Singleton, request
from service.fs.dart.exceptions import check_status


def set_api_key(api_key: str) -> str:
    DartKey().api_key = api_key
    auth = DartKey()
    return auth.api_key


def get_api_key() -> str:
    return DartKey().api_key


class DartKey(object, metaclass=Singleton):
    def __init__(self, api_key=None):
        super().__init__()
        self.__api_key = None

    @property
    def api_key(self) -> str:
        if self.__api_key is None:
            raise ValueError('Unauthorized')
        return self.__api_key

    @api_key.setter
    def api_key(self, api_key: str) -> None:
        if not isinstance(api_key, str):
            raise ValueError('The Dart Api key must be provided through the auth variable')

        verify_url = 'https://opendart.fss.or.kr/api/company.json'
        verify_payload = {'crtfc_key': api_key, 'corp_code': '00126380'}  # 00126380 : 삼성전자

        resp = request.get(url=verify_url, payload=verify_payload)
        data = resp.json()

        check_status(**data)
        self.__api_key = api_key

    def __repr__(self) -> str:
        return 'API Key: {}'.format(self.api_key)
