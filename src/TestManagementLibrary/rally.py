#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (c) 2015 Lingaro


from pyral import Rally
from robot.api import logger


class WrappedRally(Rally):
    """
    Wrapped Rally object to FIX some bugs.
    """

    def __init__(self, *args, **kwargs):
        self._project_provided = 'project' in kwargs
        super(WrappedRally, self).__init__(*args, **kwargs)

    def get(self, *args, **kwargs):
        if u'project' not in kwargs and not self._project_provided:
            kwargs['project'] = None
        return super(WrappedRally, self).get(*args, **kwargs)

    def _buildRequest(self, *args, **kwargs):
        result = super(WrappedRally, self)._buildRequest(*args, **kwargs)
        logger.info("url: " + result[2])
        return result
