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

from robot.api import logger
from pyral import Rally


class ConnectionManager(object):
    """
    Connection Manager handles the connection & disconnection to the Rally server.
    """

    def __init__(self):
        """
        Initializes _rally_connection to None.
        """
        self._rally_connection = None

    def _check_connection(self):
        """
        Checks if connection is initialized.
        """
        return not self._rally_connection is None

    def _assert_connection(self):
        """
        Checks that connection is initialized and raises a ValueError and log some info if not.
        """
        if not self._check_connection():
            logger.warn("connection have not established yet, probably you have to call connect to rally first")
            raise ValueError("connection have not established yet")

    def _get_rally_connection(self):
        """
        Safe rally connection getter.
        :return: rally connection object
        """
        self._assert_connection()
        return self._rally_connection

    def connect_to_rally(self, server, user, password, workspace=None, project=None, log_file=None):
        """
        Establishes connection to the rally server using the provided parameters: `server`, `user` and `password`.
        Optionally, you can specify a `workspace` or `project` (default values for this properties both equal 'default').

        Method can enable rally logging. You can provide optional parameter `log_file` to point file of your choice.
        Default `log_file` parameter value is None, witch indicates that logging is disabled.

        Example usage:
        | # explicitly specifies all property values |
        | Connect To Rally | SERVER_URL | USER | PASSWORD | SOME-WORKSPACE | SOME-PROJECT | PATH-TO-LOG-FILE |

        | # minimal property values set |
        | Connect To Rally | SERVER_URL | USER | PASSWORD |

        | # disable rally logging |
        | Connect To Rally | SERVER_URL | USER | PASSWORD | log_file=False |
        """
        logger.info(u"Try to connect to rally using: server={server}, workspace={workspace}, project={project}".format(
            server=server,
            workspace=workspace,
            project=project
        ))
        kwargs = {}
        if project:
            kwargs['project'] = project
        if workspace:
            kwargs['workspace'] = workspace
        self._rally_connection = Rally(server, user, password, **kwargs)
        logger.info("Connection to {server} established.".format(server=server))
        if log_file:
            self._rally_connection.enableLogging(str(log_file))
            logger.info(u"Logging to {0}".format(log_file))
        else:
            logger.info(u"Logging is disabled")
            self._rally_connection.disableLogging()

    def _reset_rally_connection(self):
        self._rally_connection = None

    def disconnect_from_rally(self):
        """
        Disconnects from the rally server.

        For example:
        | Disconnect From Rally | # disconnects from current connection to the rally |
        """
        if not self._check_connection():
            logger.info("connection doesn't exist so can't be disconnected")
        else:
            logger.info("resetting connection")
        self._reset_rally_connection()
