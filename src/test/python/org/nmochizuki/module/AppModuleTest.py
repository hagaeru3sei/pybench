# -*- coding: utf-8 -*-
import sys
sys.path.append("./src/main/python")

import fudge
from unittest import TestCase
from org.nmochizuki.variables import *
from org.nmochizuki.module.Benchmark import Benchmark
from org.nmochizuki.module.Benchmark import BenchmarkModule


class AppModuleTest(TestCase):
    app = None
    module = None
    name = ""
    params = dict()

    def setUp(self):
        self.name = "benchmark"
        self.params = dict()
        self.module = AppModule(self.name, self.params)

    def test_getModule(self):
        self.assertEquals(self.module.getModule(), BenchmarkModule)

    def test_getApp(self):
        self.assertEquals(self.module.getApp(), Benchmark)

    def test_getName(self):
        self.assertEquals(self.module.getName(), self.name)

    def test_changeModule(self):
        name = "cookie"
        cookie = (fudge.Fake('Cookie').is_callable())
        cookieModuke = (fudge.Fake('CookieModule').is_callable())
        self.module.setName(name)
        self.module.setApp(cookie)
        self.module.setModule(cookieModuke)
        self.assertEqual(self.module.getName(), name)
        self.assertEqual(self.module.getApp(), cookie)
        self.assertEqual(self.module.getModule(), cookieModuke)

    def tearDown(self):
        pass