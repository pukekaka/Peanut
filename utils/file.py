# -*- coding: utf-8 -*-
import os
import re
import zipfile
import xmltodict
from collections import OrderedDict
from typing import List


def xml_to_dict(path: str, encoding: str = 'utf8') -> OrderedDict:
    with open(path, encoding=encoding) as f:
        res = xmltodict.parse(f.read())
    return res


def unzip(file: str, path: str = None, newFolder: bool = True) -> str:
    os.path.altsep = '\\'
    head, tail = os.path.split(file)

    if path:
        extract_path = path
    else:
        extract_path = head

    with zipfile.ZipFile(file, 'r') as zip_ref:
        if newFolder:
            new_folder = tail.replace('.zip', '')
            extract_path = os.path.join(extract_path, new_folder)
        zip_ref.extractall(path=extract_path)
    return extract_path


def search_file(path: str, filename: str = None, extensions: str = 'xbrl') -> List[str]:
    file_list = []
    for root, _, files in os.walk(path):
        for file in files:
            if filename is not None and re.search(filename, file):
                file_list.append(os.path.join(root, file))
            if file.endswith('.' + extensions):
                file_list.append(os.path.join(root, file))
    return file_list


def create_folder(path: str):
    import pathlib
    try:
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    except FileExistsError:
        pass
    except OSError:
        raise


def get_cache_folder():
    from appdirs import user_cache_dir
    appname = 'dart-fss'
    cache_dir = user_cache_dir(appname)
    create_folder(cache_dir)
    return cache_dir
