# -*- coding: utf-8 -*-
from typing import Union, List

from utils import request, str_upper
from service.dart.auth import get_api_key as dart_get_api_key
from service.dart.exceptions import check_status as dart_check_status

str_or_list = Union[str, List[str]]


def search(corp_code: str = None,
           bgn_de: str = None,
           end_de: str = None,
           last_reprt_at: str = 'N',
           pblntf_ty: str_or_list = None,
           pblntf_detail_ty: str_or_list = None,
           corp_cls: str = None,
           sort: str = 'date',
           sort_mth: str = 'desc',
           page_no: int = 1,
           page_count: int = 10):

    url = 'https://opendart.fss.or.kr/api/list.json'
    api_key = dart_get_api_key()

    last_reprt_at = str_upper(last_reprt_at)
    pblntf_ty = str_upper(pblntf_ty)
    pblntf_detail_ty = str_upper(pblntf_detail_ty)

    payload = {
        'crtfc_key': api_key,
        'corp_code': corp_code,
        'bgn_de': bgn_de,
        'end_de': end_de,
        'last_reprt_at': last_reprt_at,
        'pblntf_ty': pblntf_ty,
        'pblntf_detail_ty': pblntf_detail_ty,
        'corp_cls': corp_cls,
        'sort': sort,
        'sort_mth': sort_mth,
        'page_no': page_no,
        'page_count': page_count
    }

    resp = request.get(url=url, payload=payload)
    dataset = resp.json()

    dart_check_status(**dataset)
    return dataset
