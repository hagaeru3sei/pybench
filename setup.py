# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import sys
sys.path.append('./src/main/python')
sys.path.append('./src/test/python')
print(sys.path)

def example_setup(*args, **kw):
    setup(
        name         = "Example",
        author       = "Nobuaki Mochizuki",
        author_email = "hagaeru3sei@yahoo.co.jp",
        license      = "GPL",
        description  = "README",
        version      = "0.0.1",
        packages     = find_packages(),
        test_suite   = 'example_test.suite'
    )

if __name__ == "__main__":
    try:
        example_setup()
    except Exception as e:
        print(e)
