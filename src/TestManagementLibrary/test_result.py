#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (c) 2015 Lingaro


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

        It takes 3 mandatory parameters `test_case_id` (FormattedID of test case - if list is provided it takes first
        element from list), `build` and `verdict` (allowed values are Fail or Pass).
        The last required for the test result creation parameter is `date` parameter. If it is not provided directyle
        it is set to the current datetime.

        Method takes 5 optional parameters: `notes`, `attachment_list` (a list of paths to files - absolute or relative),
        `tester` (name of the user), `test_set` (FormattedID of TestSet object) and `duration`.

        Example usage:
        | # minimal information |
        |Add Test Result | TC5001 | BUILD | Pass |
        | # standard usage |
        |Add Test Result | TC5001 | BUILD | Pass | Very complex test | ${attachment_list} |

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
