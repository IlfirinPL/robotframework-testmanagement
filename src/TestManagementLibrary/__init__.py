#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (c) 2015 Lingaro


__version__ = '0.1.10'

from .connection_manager import ConnectionManager
from .query import QueryManager
from .user import UserManager
from .attachment import AttachmentManager
from .test_case import TestCaseManager
from .test_set import TestSetManager
from .test_result import TestResultManager
from .defect import DefectManager


class TestManagementLibrary(ConnectionManager, QueryManager, UserManager, AttachmentManager, TestCaseManager,
                            TestSetManager, TestResultManager, DefectManager):
    """
    Test Management Library contains utilities meant for Robot Framework's usage.

    This can allow you to connect to the rally server and manipulate tasks.


    References:

     + Rally REST API - https://help.rallydev.com/python-toolkit-rally-rest-api

     + Robot Framework - http://robotframework.org/


    Example Usage:
    | # Setup |
    | Connect to Rally | SERVER-URL | USER | PASSWORD | WORKSPACE |
    | @{test_cases} | Find Test Case | name="ABC" |
    | # create attachments |
    | Add Test Result | @{test_cases} | BUILD-NAME | VERDICT | NOTES | attachment_list=${attachment_list} |
    | # do something more ... |
    | Disconnect form Rally |
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
