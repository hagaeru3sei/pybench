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

    def tearDown(self):
        pass


def suite():
    ts = TestSuite()
    tests = [BenchmarkModuleTest]

    ts.addTests(map(makeSuite, tests))

    return ts

