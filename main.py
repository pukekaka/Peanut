# -*- coding: utf-8 -*-
import service.info as info_service
import service.fs.dart as dart_service


if __name__ == '__main__':
    # KRX Company List
    corp_list = info_service.get_corp_list()

    # DART API
    api_key = input('Input API_KEY: ')
    dart_service.set_api_key(api_key=api_key)


