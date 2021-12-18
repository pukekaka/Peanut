# -*- coding: utf-8 -*-
import re

from utils import request
from service.fs.dart.auth import get_api_key as dart_get_api_key
from service.fs.dart.exceptions import check_status as dart_check_status


def get_corp_profile(corp_code: str):
    corp_code_checker = re.compile(r'^[0-9]{8}$')
    if corp_code and corp_code_checker.search(corp_code) is None:
        raise ValueError('corp_code must be 8 digits')

    url = 'https://opendart.fss.or.kr/api/company.json'
    api_key = dart_get_api_key()

    payload = {
        'crtfc_key': api_key,
        'corp_code': corp_code,
    }

    resp = request.get(url=url, payload=payload)
    dataset = resp.json()

    dart_check_status(**dataset)
    return dataset
