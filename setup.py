#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (c) 2015 Lingaro


"""Setup script for Robot's TestManagementLibrary distributions"""

from setuptools import setup

setup(
    name=u'robotframework-testmanagement',
    version=u'0.1.1',
    description=u'Test management utility library for Robot Framework',
    author=u'Michał Lula',
    author_email=u'michal.lula@lingaro.com',
    url=u'https://github.com/IlfirinPL/robotframework-testmanagement',
    download_url=u'https://github.com/IlfirinPL/robotframework-testmanagement/tarball/0/1',
    keywords=['robotframework', 'rally', 'pyral'],
    package_dir={u'': 'src'},
    packages=['TestManagementLibrary'],
    install_requires=[
        u'robotframework',
        u'requests',
        u'pyral'
    ]
)
