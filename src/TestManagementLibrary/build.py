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

from .query import (
    Operator,
    ObjectIDParameter
)


class BuildManager(object):
    """
    We assumes that this class will be mixed with RallyConnectionManager to provide the _get_rally_connection method.
    """

    def add_build(self):
        """
        Not implemented.
        """
        raise NotImplementedError()

    def modify_build(self):
        """
        Not implemented.
        """
        raise NotImplementedError()

    def remove_build(self):
        """
        Not implemented.
        """
        raise NotImplementedError()

    def _get_build(self, query, **kwargs):
        """
        Calls Rally Rest API with given query and fetch build object
        :param query: RallyQuery object
        :return: Build object
        """
        return self._execute_rally_query(u'Build', query, fetch=True, **kwargs)

    def _get_build_by_id(self, object_id):
        return self._get_object_by_id(u'Build', ObjectIDParameter(object_id, Operator.EQUAL))

    def find_build(self, object_id=None, join_method=None):
        """
        @TODO:
        """
        query = self._build_query(
            param_join_method=join_method,
            object_id=object_id
        )
        result = self._get_build(query)
        return [item.ObjectID for item in result]