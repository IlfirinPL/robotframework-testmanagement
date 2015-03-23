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

import urlparse

from robot.api import logger


def get_first(value_or_list):
    if isinstance(value_or_list, (list, tuple)):
        if value_or_list:
            logger.info(u"List provided so get first: {0}".format(value_or_list[0]))
            value = value_or_list[0]
        else:
            logger.warn(u"Empty list.")
            raise ValueError(u"Empty list")
    else:
        value = value_or_list
    return value


def get_netloc_and_path( url):
    split_result = urlparse.urlsplit(url)
    if split_result.scheme and split_result.scheme != u'https':
        raise ValueError(u"unsupported protocol {0}. Only https is allowed".format(split_result.scheme))
    result = split_result.netloc + split_result.path
    logger.info(u"Extracted netloc and path {0} from {1}".format(result, url))
    return result
