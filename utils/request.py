# -*- coding: utf-8 -*-
import requests
import fake_useragent
import time
import re

from utils import Singleton
from utils import cache


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

    def download(self,
                 url: str,
                 path: str,
                 filename: str = None,
                 method: str = 'GET',
                 payload: dict = None,
                 referer: str = None,
                 timeout: int = 120) -> dict:
        from utils.spinner import Spinner
        from utils.file import create_folder
        from urllib.parse import unquote
        import os

        create_folder(path)

        r = self.request(url=url, method=method, payload=payload, referer=referer, stream=True, timeout=timeout)

        headers = r.headers.get('Content-Disposition')
        if headers is None or not re.search('attachment', headers):
            raise FileNotFoundError('target does not exist')

        # total_size = int(r.headers.get('content-length', 0))
        block_size = 8192

        # Extract filename
        extracted_filename = unquote(re.findall(r'filename="?([^"]*)"?', headers)[0])

        if filename is None:
            filename = extracted_filename
        else:
            filename = filename.format(extracted_filename)

        spinner = Spinner('Downloading ' + filename)
        spinner.start()

        file_path = os.path.join(path, filename)
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=block_size):
                if chunk is not None:
                    f.write(chunk)
        r.close()
        spinner.stop()
        return {'filename': filename, 'path': path, 'full_path': file_path}


request = Request()
