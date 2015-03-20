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
import mimetypes


class AttachmentManager(object):
    """
    We assumes that this class will be mixed with RallyConnectionManager to provide the _get_rally_connection method.
    """

    @classmethod
    def _build_attachment_data(cls, attachment):
        mime_type, _ = mimetypes.guess_type(attachment, strict=False)
        if not mime_type:
            logger.warn(u"can't guess mime type for {0}".format(attachment))
        return dict(
            Name=attachment,
            mime_type=mime_type
        )

    @classmethod
    def _build_attachment_list_data(cls, attachment_list=None):
        return [cls._build_attachment_data(attachment) for attachment in attachment_list or ()]

    def _add_attachments(self, artifact, attachment_list):
        """
        Calls Rally Rest API with given query and fetch build object
        :param query: RallyQuery object
        :return: Build object
        """
        attachment_list_data = self._build_attachment_list_data(attachment_list)
        if attachment_list:
            logger.info("Adding attachments:")
            conn = self._get_rally_connection()
            conn.addAttachments(artifact, attachment_list_data)
