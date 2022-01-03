# -*- coding: utf-8 -*-
from utils import request

from service.dart.auth import get_api_key as dart_get_api_key


def download_document(path: str, rcept_no: str) -> str:
    url = 'https://opendart.fss.or.kr/api/document.xml'

    api_key = dart_get_api_key()
    payload = {
        'crtfc_key': api_key,
        'rcept_no': rcept_no,
    }

    resp = request.download(url=url, path=path, payload=payload)
    return resp['full_path']
