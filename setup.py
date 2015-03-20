#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (c) 2015 Lingaro
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


"""Setup script for Robot's TestManagementLibrary distributions"""

from setuptools import setup, find_packages


setup(
    name=u'robotframework-testmanagement-library',
    version=u'0.1',
    description=u'Test management utility library for Robot Framework',
    author=u'Michał Lula',
    author_email=u'michal.lula@lingaro.com',
    url=u'https://github.com/IlfirinPL/robotframework-testmanagement',
    package_dir={u'': 'src'},
    packages=['TestManagementLibrary'],
    install_requires=[
        u'robotframework',
        u'requests',
        u'pyral'
    ]
)
