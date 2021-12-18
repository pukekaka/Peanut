# -*- coding: utf-8 -*-
import service.info as info_service
import service.fs.dart as dart_service


if __name__ == '__main__':
    # DART API
    api_key = input('[DART] Input API_KEY: ')
    dart_service.set_api_key(api_key=api_key)

    # Get Company List
    corp_list = info_service.get_corp_list()

    # get executive shareholder
    samsung = corp_list.find_by_corp_code('00126380')

    executive_shareholder = samsung.get_executive_shareholder()
    majority_shareholder = samsung.get_majority_shareholder()


