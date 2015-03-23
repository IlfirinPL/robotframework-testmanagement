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


class TestCaseManager(object):
    """
    We assumes that this class will be mixed with RallyConnectionManager to provide the _get_rally_connection method.
    """

    def _get_test_case(self, query, **kwargs):
        """
        Calls Rally Rest API with given query
        :param query: RallyQuery object
        :return:
        """
        return self._execute_rally_query(u'TestCase', query, fetch=True, **kwargs)

    def _get_test_case_by_id(self, formatted_id):
        """
        Gets test_case with given FormattedID
        :param formatted_id:
        :return:
        """
        return self._get_object_by_id(u'TestCase', FormattedIDParameter(formatted_id, Operator.EQUAL))

    def find_test_case(self, formatted_id=None, project=None, name=None, description=None, notes=None, join_method=None):
        """
        Finds test cases base on criteria provided as a method parameters. All parameters are optional. If you don't
        provide value the parameter won't be used in created query. So far `formatted_id`, `project`, `name`,
        `description` and `notes` are supported.
        For parameters `formatted_id`, `name`, `description` and `notes` the contains operator is applied.
        For parameter `project` the `=` operator is applied.
        You can specify the parameter `join_method` witch indicate how to concatenate parameters. This parameter accepts
        values: AND, OR. The method is applied to all parameters. Default value is AND.

        Returns list of founded FormattedId of Test Cases that meets the search criteria.

        Example usage:
        | # find test case by FormattedId |
        | Find Test Case | T28 |

        | # find test case by FormattedId and Name |
        | Find Test Case | T2 | | SOME-NAME |

        | # find test case by FormattedId or Name |
        | Find Test Case | T2 | | SOME-NAME | | | OR |
        """
        query = self._build_query(
            param_join_method=join_method,
            formatted_id=formatted_id,
            project=project,
            name=name,
            description=description,
            notes=notes
        )
        result = self._get_test_case(query)
        return [item.FormattedID for item in result]
