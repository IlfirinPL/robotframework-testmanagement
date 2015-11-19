#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (c) 2015 Lingaro

import traceback
import socket

from robot.api import logger
from .utils import get_netloc_and_path
from .rally import WrappedRally


class ConnectionManager(object):
    """
    Connection Manager handles the connection & disconnection to the Rally server.
    """

    RALLY_CONNECTION_CLASS = WrappedRally
    INVALIND_CREDENTIALS_MESSAGE = u'Invalid credentials'

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

    def _create_rally_connection(self, *args, **kwargs):
        logger.debug("timeout before really connection creation: {0}".format(socket.getdefaulttimeout()))
        old_timeout = socket.getdefaulttimeout()
        try:
            return self.RALLY_CONNECTION_CLASS(*args, **kwargs)
        finally:
            logger.debug("timeout changed to: {0}".format(socket.getdefaulttimeout()))
            socket.setdefaulttimeout(old_timeout)
            logger.debug("Back to previous value: {0}".format(socket.getdefaulttimeout()))

    def _detect_wrong_credentials(self, err):
        """
        Detects if error is related to invalid credentials passed by the user. This check is useful to not retry and to
        not block the user account.
        Args:
            err:

        Returns: True if error is related to invalid credentials and False otherwise
        """
        return self.INVALIND_CREDENTIALS_MESSAGE in err.message

    def connect_to_rally(self, server_url, user, password, workspace, project=None, number_of_retries=3, log_file=None):
        """
        Establishes connection to the rally server using the provided parameters: `server`, `user` and `password`.
        You have to specify a `workspace` parameter to set the correct workspace environment. You may set `project`
        parameter, but it is optional (default None means to search in all projects in workspace).

        You may provided `number_of_retries` parameter witch indicate how many times we should try to establish
        connections. Default value is 3. If `number_of_retries` is reach the last exception is thrown. All exceptions
        occurred in previous tries are swallowed.

        Method can enable rally logging. You can provide optional parameter `log_file` to point file of your choice.
        Default `log_file` parameter value is None, witch indicates that logging is disabled.

        Example usage:
        | # explicitly specifies all property values |
        | Connect To Rally | SERVER_URL | USER | PASSWORD | SOME-WORKSPACE | SOME-PROJECT | NUMBER-OF-RETRIES | PATH-TO-LOG-FILE |

        | # minimal property values set |
        | Connect To Rally | SERVER_URL | USER | PASSWORD | WORKSPACE |

        | # minimal with logging logging enabled |
        | Connect To Rally | SERVER_URL | USER | PASSWORD | WORKSPACE | log_file=False |
        """
        logger.info(u"Try to connect to rally using: server={server}, workspace={workspace}, project={project}".format(
            server=server_url,
            workspace=workspace,
            project=project
        ))
        server = get_netloc_and_path(server_url)
        kwargs = {}
        if project:
            kwargs['project'] = project
        if workspace:
            kwargs['workspace'] = workspace
        tries_counter = 0

        number_of_retries = int(number_of_retries)

        while True:
            tries_counter += 1
            try:
                self._rally_connection = self._create_rally_connection(server, user, password, **kwargs)
                break
            except Exception as e:
                if self._detect_wrong_credentials(e):
                    logger.error(self.INVALIND_CREDENTIALS_MESSAGE)
                    raise e
                elif number_of_retries <= tries_counter:
                    logger.warn("An error occurred. Maximum number of tries reached.")
                    raise e
                else:
                    logger.warn("An error occurred. Try again.")
                    logger.warn(traceback.format_exc())

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
