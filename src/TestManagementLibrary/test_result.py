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
import datetime
import traceback

from robot.api import logger


class TestResultManager(object):

    def _build_test_result_data(self, build_id, test_case_id, verdict, date=None, tester=None, test_set=None,
                                notes=None, duration=None, attachment_list=None):
        """
        :param test_case_ID:
        :param verdict:
        :param build:
        :param date:
        :param tester:
        :param test_set:
        :param notes:
        :param duration:
        :param attachment_list:
        :return:
        """
        test_case = self._get_test_case_by_id(test_case_id)
        build = self._get_build_by_id(build_id)
        return dict(
            TestCase=test_case.ref,
            Build=build.ref,
            Verdict=verdict,
            Date=datetime.datetime.now().isoformat()
        )

    # def _create_build_definition(self, connection):
    #     return connection.create('BuildDefinition', dict(
    #         Project=connection.getProject().ref,
    #         Name=u"Ala ma kota"
    #     ))
    #
    # def _create_build(self, connection, build_definition):
    #     return connection.create('Build', dict(
    #         BuildDefinition=build_definition.ref,
    #         Status=u"SUCCESS"
    #     ))

    def _get_first(self, value_or_list):
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

    def add_test_result(self, test_case, build, verdict, date=None, tester=None, test_set=None, notes=None, duration=None, attachment_list=None):
        """
        Adds a new Test Result to Test Case provided with FormatterID passed as first (obligatory) parameter.
        """
        logger.info(u"Provided test case FormattedID: {0}".format(unicode(test_case)))
        logger.info(u"Provided build ObjectID: {0}".format(unicode(build)))
        test_case_id = self._get_first(test_case)
        build_id = self._get_first(build)
        connection = self._get_rally_connection()
        try:
            return connection.create('TestCaseResult', self._build_test_result_data(build_id, test_case_id, verdict))
        except Exception as e:
            logger.warn("An error occurred")
            logger.warn(traceback.format_exc())
            raise e

