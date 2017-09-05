# -*- coding: utf-8 -*-
import threading
import logging
import random
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from org.nmochizuki.AppContext import AppContext
from org.nmochizuki.decorators import *


class Benchmark(AppContext):

    max_workers = 1
    count = 1
    url = ""
    method = ""
    result = dict()
    timeout = 60
    qps = 10
    request = None
    urls = []
    useragents = []
    cookies = []
    logger = logging.getLogger(__name__)

    def __init__(self, module, params):
        """ """

        self.logger.info(params)

        AppContext.__init__(self)

        if not params['method']:
            params['method'] = BenchmarkModule.method

        module = module() \
            .set_url(params['url']) \
            .set_count(params['count']) \
            .set_max_workers(params['worker']) \
            .set_qps(params['qps']) \
            .set_method(params['method'])

        self.max_workers = module.get_max_workers()
        self.url = module.get_url()
        self.count = module.get_count()
        self.method = module.get_method()
        self.timeout = 1.0

        self.load_useragents()
        self.load_urls()
        self.load_cookies()

        self.init_result()
        self.init_request()

    def init_result(self):
        """ """
        self.result['success'] = 0
        self.result['error'] = 0
        self.result['message'] = ""
        self.result['avg_time'] = 0.0
        self.result['max_time'] = 0.0
        self.result['min_time'] = 0.0
        self.result['result_time'] = 0.0
        self.result['total'] = 0
        self.result['start'] = time.time()
        self.result['end'] = 0.0

    def init_request(self):
        """ """
        self.request = Request(self.url)
        self.request.method = self.method
        self.request.add_header('Accept-Encoding', 'gzip, deflate')
        self.request.add_header('Connection', 'keep-alive')
        self.request.add_header('Cookie', '; '.join(self.cookies))

    def load_useragents(self):
        """" """
        with open('src/main/resources/useragents.txt') as fh:
            self.useragents = [ua.rstrip() for ua in fh]

    def load_cookies(self):
        """ """
        with open('src/main/resources/cookies.txt') as fh:
            self.cookies = [cookie.rstrip() for cookie in fh]

    def load_urls(self):
        """ """
        with open('src/main/resources/urls.txt') as fh:
            self.urls = [url.rstrip() for url in fh]

    def execute(self):
        """ """
        with ThreadPoolExecutor(self.max_workers) as executor:
            for i in range(self.count):
                self.request.add_header('User-Agent', str(random.sample(self.useragents, 1)[0]))
                executor.submit(self.url_request, self.request, self.timeout)

    @classmethod
    def url_request(cls, request, timeout):
        """ return None """
        start = time.time()

        cls.logger.debug("thread:%s started." % (threading.current_thread(),))

        try:
            with urlopen(request, timeout=timeout) as rs:
                if rs.status != 200:
                    raise URLError("status:%d" % (rs.status,))
        except Exception as e:
            cls.logger.error(e)
            cls.result['message'] = e
            cls.result['error'] += 1
            cls.result['total'] += 1
            raise RuntimeError(e)

        cls.result['result_time'] = time.time() - start
        if cls.result['max_time'] <= cls.result['result_time']:
            cls.result['max_time'] = cls.result['result_time']
        if cls.result['min_time'] >= cls.result['result_time'] or cls.result['min_time'] == 0.0:
            cls.result['min_time'] = cls.result['result_time']
        cls.result['success'] += 1
        cls.result['total'] += 1
        cls.result['avg_time'] = ((cls.result['avg_time'] * cls.result['total'])
                                  + cls.result['result_time']) / (cls.result['total'] + 1)

        if cls.result['total'] > 0 and cls.result['total'] % 100 == 0:
            cls.logger.info("request passed %d." % (cls.result['total'],))

        if cls.result['avg_time'] == 0.0:
            cls.result['avg_time'] = cls.result['result_time']

        cls.logger.debug("thread:%s finished." % (threading.current_thread(),))

    def __del__(self):
        self.result['end'] = time.time()
        self.result['exec_time'] = self.result['end'] - self.result['start']
        self.logger.info(self.result)


class BenchmarkModule(object):
    """ """
    url = ""
    count = 1
    max_workers = 1
    qps = 1
    method = "GET"

    def __init__(self):
        self.url = ""
        self.count = 1
        self.max_workers = 1
        self.qps = 1
        self.method = "GET"

    def set_url(self, url):
        self.url = url
        return self

    def set_count(self, count):
        self.count = count
        return self

    def set_max_workers(self, max_workers):
        self.max_workers = max_workers
        return self

    def set_qps(self, qps):
        self.qps = qps
        return self

    def set_method(self, method):
        self.method = method
        return self

    def get_url(self):
        return self.url

    def get_count(self):
        return self.count

    def get_max_workers(self):
        return self.max_workers

    def getQPS(self):
        return self.qps

    def get_method(self):
        return self.method
