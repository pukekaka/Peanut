# -*- coding: utf-8 -*-
import requests
import fake_useragent
import time

from dart.utils import Singleton
from dart.utils import cache


@cache()
def get_user_agent():
    ua = fake_useragent.UserAgent()
    agent = ua.chrome
    return str(agent)


class Request(object, metaclass=Singleton):
    def __init__(self):
        self.s = requests.Session()
        self.update_user_agent()
        self.delay = 0.2

    def update_user_agent(self, force: bool = False):
        if force:
            ua = fake_useragent.UserAgent()
            agent = ua.chrome
            user_agent = str(agent)
        else:
            user_agent = get_user_agent()
        self.s.headers.update({'user-agent': user_agent})

    def request(self,
                url: str,
                method: str = 'GET',
                payload: dict = None,
                referer: str = None,
                stream: bool = False,
                timeout: int = 120):
        headers = self.s.headers
        if referer is not None:
            headers['referer'] = referer

        req = requests.Request(method, url=url, params=payload, headers=headers)
        prepped = self.s.prepare_request(req)
        resp = self.s.send(prepped, stream=stream, timeout=timeout)
        if self.delay is not None:
            time.sleep(self.delay)
        return resp

    def get(self,
            url: str,
            payload: dict = None,
            referer: str = None,
            stream: bool = False,
            timeout: int = 120):
        return self.request(url=url, method='GET', payload=payload, referer=referer, stream=stream, timeout=timeout)

    def post(self,
             url: str,
             payload: dict = None,
             referer: str = None,
             stream: bool = False,
             timeout: int = 120):
        return self.request(url=url, method='POST', payload=payload, referer=referer, stream=stream, timeout=timeout)


request = Request()
