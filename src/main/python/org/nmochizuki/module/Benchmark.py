# -*- coding: utf-8 -*-
import time
import threading
import logging
from urllib.error import HTTPError
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from org.nmochizuki.AppContext import AppContext


class Benchmark(AppContext):
    max_workers = 1
    count = 1
    url = ""
    method = ""
    result = dict()
    timeout = 1.0
    qps = 10
    request = None
    urls = []
    useragents = []
    logger = logging.getLogger(__name__)

    def __init__(self, module, params):
        """ """

        self.logger.info(params)

        AppContext.__init__(self)

        if not params['method']:
            params['method'] = BenchmarkModule.method

        module = module() \
            .setUrl(params['url']) \
            .setCount(params['count']) \
            .setMaxWorkers(params['worker']) \
            .setQPS(params['qps']) \
            .setMethod(params['method'])

        self.max_workers = module.getMaxWorkers()
        self.url = module.getUrl()
        self.count = module.getCount()
        self.method = module.getMethod()
        self.timeout = 1.0

        self.loadUserAgents()
        self.loadURLs()

        self.initResult()
        self.initRequest()

    def initResult(self):
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

    def initRequest(self):
        """ """
        self.request = Request(self.url)
        self.request.method = self.method
        self.request.add_header('Accept-Encoding', 'gzip, deflate')
        self.request.add_header('Connection', 'keep-alive')
        self.request.add_header('User-Agent', 'Mozilla/5.0')

    def rebindRequest(self, useragent):
        """ return Request request """
        #request.full_url = random.sample(urls, 1)
        self.request.add_header('User-Agent', useragent)
        return self.request

    def loadUserAgents(self):
        """ """
        with open('src/main/resources/useragent.txt') as fh:
            self.useragents = [ua.rstrip() for ua in fh]

    def loadURLs(self):
        """ """
        with open('src/main/resources/request.txt') as fh:
            self.urls = [url.rstrip() for url in fh]

    def execute(self):
        """ """
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            try:
                for i in range(self.count):
                    #self.rebindRequest(random.sample(self.useragents, 1))
                    executor.submit(self.urlRequest, self.request, self.timeout)

            except RuntimeError as e:
                self.logger.error(e)
                self.result['message'] = e
                self.result['error'] += 1
                self.result['total'] += 1

            except Exception as e:
                self.logger.error(e)

    @classmethod
    def urlRequest(cls, request, timeout, useragent="", url=""):
        """ return None """
        start = time.time()

        cls.logger.debug("thread:%s started." % (threading.current_thread(),))

        try:
            with urlopen(request, timeout=timeout) as rs:
                if rs.status != 200:
                    raise URLError("status:%d" % (rs.status,))

        except URLError as e:
            cls.logger.error(e)
            cls.result['message'] = e
            cls.result['error'] += 1
            cls.result['total'] += 1
            raise RuntimeError(e)

        except HTTPError as e:
            cls.logger.error(e)
            cls.result['message'] = e
            cls.result['error'] += 1
            cls.result['total'] += 1
            raise RuntimeError(e)

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

    def setUrl(self, url):
        self.url = url
        return self

    def setCount(self, count):
        self.count = count
        return self

    def setMaxWorkers(self, max_workers):
        self.max_workers = max_workers
        return self

    def setQPS(self, qps):
        self.qps = qps
        return self

    def setMethod(self, method):
        self.method = method
        return self

    def getUrl(self):
        return self.url

    def getCount(self):
        return self.count

    def getMaxWorkers(self):
        return self.max_workers

    def getQPS(self):
        return self.qps

    def getMethod(self):
        return self.method
