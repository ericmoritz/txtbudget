#!/usr/bin/env python

from setuptools import setup
import txtbudget

setup(name='txtbudget',
      version=txtbudget.__version__,
      description='Text based budget scheduler',
      author='Eric Moritz',
      author_email='eric@themoritzfamily.com',
      scripts=['bin/txtbudget',],
      packages=['txtbudget',],
      install_requires=[
          "dateutils"
      ],
      test_suite="txtbudget.tests",
     )
