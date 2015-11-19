#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (c) 2015 Lingaro


from .query import (
    FormattedIDParameter,
    Operator
)


class TestSetManager(object):
    """
    We assumes that this class will be mixed with RallyConnectionManager to provide the _get_rally_connection method.
    """

    def _get_test_set_by_id(self, formatted_id, *args, **kwargs):
        """
        Gets test set by id
        :param formatted_id:
        :return:
        """
        return self._get_object_by_id(u'TestSet', FormattedIDParameter(formatted_id, Operator.EQUAL),
                                      *args, **kwargs)
