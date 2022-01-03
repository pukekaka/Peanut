# -*- coding: utf-8 -*-
from utils.cache import cache
from utils.singleton import Singleton
from utils.request import request, get_user_agent
from utils.notebook import dict_to_html, is_notebook
from utils.spinner import Spinner, spinner_enable
from utils.file import unzip, xml_to_dict, search_file, create_folder, get_cache_folder
from utils.dataframe import dataframe_astype
from utils.string import str_upper

__all__ = [
    'cache',
    'Singleton',
    'get_user_agent', 'request',
    'dict_to_html', 'is_notebook',
    'Spinner', 'spinner_enable',
    'unzip', 'xml_to_dict', 'search_file', 'create_folder', 'get_cache_folder',
    'dataframe_astype',
    'str_upper',
]
