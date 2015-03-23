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

import traceback
from TestManagementLibrary.query import Operator

from .query import (
    FormattedIDParameter
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
        return self._get_object_by_id(u'TestCase', FormattedIDParameter(formatted_id, operator=Operator.EQUAL),
                                      *args, **kwargs)
