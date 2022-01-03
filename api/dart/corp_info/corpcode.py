# -*- coding: utf-8 -*-
from collections import OrderedDict

from utils import request, unzip, get_cache_folder, search_file, xml_to_dict
from service.dart.auth import get_api_key as dart_get_api_key


def get_corp_code() -> OrderedDict:
    import tempfile

    with tempfile.TemporaryDirectory() as path:
        url = 'https://opendart.fss.or.kr/api/corpCode.xml'

        api_key = dart_get_api_key()
        payload = {'crtfc_key': api_key}

        resp = request.download(url=url, path=path, payload=payload)
        download_path = resp['full_path']
        cache_folder = get_cache_folder()

        unzip_path = unzip(file=download_path, path=cache_folder)

        files = search_file(path=unzip_path, filename='CORPCODE', extensions='xml')
        if len(files) == 0:
            raise FileNotFoundError('CORPCODE.xml Not Found')

        file = files[0]
        data = xml_to_dict(file)
        return data['result']['list']
