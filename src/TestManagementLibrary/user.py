#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (c) 2015 Lingaro


from .query import (
    Operator,
    DisplayNameParameter
)


class UserManager(object):
    """
    We assumes that this class will be mixed with RallyConnectionManager to provide the _get_rally_connection method.
    """

    def _get_user(self, query, **kwargs):
        """
        Calls Rally Rest API with given query and fetch build object
        :param query: RallyQuery object
        :return: Build object
        """
        return self._execute_rally_query(u'User', query, fetch=True, **kwargs)

    def _get_user_by_name(self, name):
        return self._get_object_by_id(u'User', DisplayNameParameter(name, Operator.EQUAL))
