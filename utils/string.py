# -*- coding: utf-8 -*-

def str_upper(strings):
    if strings is None:
        return strings
    elif isinstance(strings, str):
        return strings.upper()
    elif isinstance(strings, list):
        return [x.upper() for x in strings]
    else:
        raise ValueError('invalid type')