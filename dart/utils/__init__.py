# -*- coding: utf-8 -*-
from dart.utils.cache import cache
from dart.utils.singleton import Singleton
from dart.utils.request import get_user_agent, request


__all__ = [
    'cache',
    'Singleton',
    'get_user_agent', 'request',
]