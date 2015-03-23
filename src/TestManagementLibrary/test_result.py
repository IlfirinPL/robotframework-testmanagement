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

from .utils import get_first

class TestResultManager(object):

    def _build_test_result_data(self, test_case_id, build, verdict, date=None, tester=None, test_set=None,
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
        result = dict(
            TestCase=test_case.ref,
            Build=build,
            Verdict=verdict,
            Date=date or datetime.datetime.now().isoformat()
        )
        if tester:
            user = self._get_user_by_name(tester)
            result['Tester'] = user.ref
        if test_set:
            test_set = self._get_test_set_by_id(test_set)
            result['TestSet'] = test_set.ref
        if notes:
            result['Notes'] = notes
        if duration:
            result['Duration'] = duration
        return result

    def add_test_result(self, test_case_id, build, verdict, notes=None, attachment_list=None, date=None, tester=None,
                        test_set=None, duration=None):
        """
        Adds a new Test Result to Test Case provided with FormatterID passed as first (obligatory) parameter.
        """
        logger.info(u"""Add test result:
        FormattedID: {test_case_id}
        Build: {build}
        Verdict: {verdict}
        Date: {date}
        Tester: {tester}
        TestSet: {test_set}
        Notes: {notes}
        Duration: {duration}
        Attachment_list: {attachment_list}""".format(
            test_case_id=test_case_id,
            build=build,
            verdict=verdict,
            date=date,
            tester=tester,
            test_set=test_set,
            notes=notes,
            duration=duration,
            attachment_list=attachment_list
        ))
        test_case_id = get_first(test_case_id)
        connection = self._get_rally_connection()
        test_result_data = self._build_test_result_data(test_case_id, build, verdict,
                                                        date=date, tester=tester, test_set=test_set, notes=notes,
                                                        duration=duration)
        try:
            test_result = connection.create('TestCaseResult', test_result_data)
            self._add_attachments(test_result, attachment_list)
        except Exception as e:
            logger.warn("An error occurred")
            logger.warn(traceback.format_exc())
            raise e
