#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (c) 2015 Lingaro


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


def make_tuple(value_or_list):
    result = None
    if not value_or_list:
        result = ()
    elif isinstance(value_or_list, (list, tuple)):
        result = value_or_list
    else:
        result = (value_or_list,)
    return result


def get_netloc_and_path( url):
    split_result = urlparse.urlsplit(url)
    if split_result.scheme and split_result.scheme != u'https':
        raise ValueError(u"unsupported protocol {0}. Only https is allowed".format(split_result.scheme))
    result = split_result.netloc + split_result.path
    logger.info(u"Extracted netloc and path {0} from {1}".format(result, url))
    return result
