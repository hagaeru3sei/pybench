# -*- coding:utf-8 -*-
import sys
sys.path.append("./src/main/python")
import fudge
from unittest import TestCase
from unittest import TestSuite
from unittest import makeSuite
from unittest import skip
from org.nmochizuki.variables import *
from org.nmochizuki.Controller import Controller
from org.nmochizuki.decorators import synchronized
from org.nmochizuki.module.Benchmark import Benchmark
from org.nmochizuki.module.Benchmark import BenchmarkModule

class BenchmarkModuleTest(TestCase):

    app = None
    module = None

    def setUp(self):
        #self.module = fudge.Fake('BenchmarkModule').is_a_stub()
        self.module = BenchmarkModule()

    def test_getUrl_defaultValue(self):
        self.assertEqual(self.module.getUrl(), '')

    def test_getCount_defaultValue(self):
        self.assertEqual(self.module.getCount(), 1)

    def test_getMaxWorkers_defaultValue(self):
        self.assertEqual(self.module.getMaxWorkers(), 1)

    def test_getQPS_defaultValue(self):
        self.assertEqual(self.module.getQPS(), 1)

    def test_getMethod_defaultValue(self):
        self.assertEqual(self.module.getMethod(), 'get')

    def test_module_getUrl(self):
        url = "http://localhost"
        self.module.setUrl(url)
        self.assertEqual(self.module.getUrl(), url)

    def test_module_getCount(self):
        count = 10
        self.module.setCount(count)
        self.assertEqual(self.module.getCount(), count)

    def test_module_getMaxWorkers(self):
        worker = 2
        self.module.setMaxWorkers(worker)
        self.assertEqual(self.module.getMaxWorkers(), worker)

    def test_module_getQPS(self):
        qps = 10
        self.module.setQPS(qps)
        self.assertEqual(self.module.getQPS(), qps)

    #def test_setUrl_return(self):
    #    self.assertIs(type(self.module), self.module.setUrl('http://localhost'))

    #def test_setCount_return(self):
    #    self.assertIs(type(self.module), self.module.setCount(1))

    #def test_setMaxWorkers_return(self):
    #    self.assertIs(type(self.module), self.module.setMaxWorkers(1))

    #def test_setQPS_return(self):
    #    self.assertIs(type(self.module), self.module.setQPS(1))

    #def test_setMethod_return(self):
    #    self.assertIs(type(self.module), self.module.setMethod('get'))

    @skip('exception test skipping')
    def test_ControllerException(self):
        try:
            controller = Controller()
            if not controller:
                raise Exception('get controller instance error.')
        except Exception as e:
            self.assertTrue(e)

    @skip('app test skipping')
    def test_app_getInstance(self):
        pass

    def tearDown(self):
        pass


class ControllerTest(TestCase):

    module = None
    params = {}

    def setUp(self):
        self.params = {}
        try:
            injector.binder.bind(AppName, 'benchmark')
            injector.binder.bind(AppParams, self.params)

            ctrl = (fudge.Fake('Controller').is_callable().expects('setModule'))
            ctrl.setModule(injector.get(AppModule))
            self.module = ctrl.getModule()
        except Exception as e:
            self.assertFalse(e)

    @skip('skip')
    def test_isAppModule(self):
        self.assertIs(type(self.module), AppModule)

    @skip('skip')
    def test_isBenchMarkApp(self):
        benchmark = (fudge.Fake('Benchmark').is_callable().expects('__init__'))
        self.assertIsInstance(benchmark, self.module.get())

    @skip('skip')
    def test_urlRequest(self):
        self.module.get().urlRequest()

    def tearDown(self):
        pass


def suite():
    ts = TestSuite()
    tests = [BenchmarkModuleTest, ControllerTest]

    ts.addTests(map(makeSuite, tests))

    return ts

