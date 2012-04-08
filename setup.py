#!/usr/bin/env python
# coding: utf-8

# Define __version__ without importing msgpackrpc.
# This allows building sdist without installing any 3rd party packages.
exec(open('msgpackrpc/_version.py').read())

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='msgpack-rpc-python',
      version=__version__,
      author='Masahiro Nakagawa',
      author_email='repeatedly@gmail.com',
      url="https://github.com/msgpack/msgpack-rpc-python",
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
      )
