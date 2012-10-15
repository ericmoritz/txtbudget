#!/usr/bin/env python

from setuptools import setup

setup(name='txtbudget',
      version='1.0.2',
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
