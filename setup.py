#!/usr/bin/env python
# coding: utf-8

import distutils.core
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    setup = distutils.core.setup
    pass

kwargs = {}
major, minor = sys.version_info[:2]
if major >= 3:
    import setuptools  # setuptools is required for use_2to3
    kwargs["use_2to3"] = True

setup(name='msgpack-rpc-python',
      version='0.2.1',
      author='Masahiro Nakagawa',
      author_email='repeatedly@gmail.com',
      url="https://github.com/msgpack/msgpack-rpc",
      description="MessagePack RPC",
      long_description="""\
MessagePack RPC for Python.

This implementation uses Tornado framework as a backend.
""",
      packages=['msgpackrpc', 'msgpackrpc/transport'],
      install_requires=['msgpack-python', 'tornado'],
      license="Apache Software License",
      classifiers=[
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: Apache Software License'],
      **kwargs
      )
