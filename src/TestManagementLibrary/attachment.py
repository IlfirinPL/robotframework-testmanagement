#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (c) 2015 Lingaro


from robot.api import logger
import mimetypes

from .utils import make_tuple

class AttachmentManager(object):
    """
    We assumes that this class will be mixed with RallyConnectionManager to provide the _get_rally_connection method.
    """

    @classmethod
    def _build_attachment_data(cls, attachment, default_mime_type='binary/octet-stream'):
        mime_type, _ = mimetypes.guess_type(attachment, strict=False)
        if not mime_type:
            mime_type = default_mime_type
            logger.warn(u"can't guess mime type for {0}, use default: {1}".format(attachment, mime_type))
        return dict(
            Name=attachment,
            mime_type=mime_type
        )

    @classmethod
    def _build_attachment_list_data(cls, attachment_list=None):
        return [cls._build_attachment_data(attachment) for attachment in make_tuple(attachment_list)]

    def _add_attachments(self, artifact, attachment_list):
        """
        Calls Rally Rest API with given query and fetch build object
        :param query: RallyQuery object
        :return: Build object
        """
        attachment_list_data = self._build_attachment_list_data(attachment_list)
        if attachment_list:
            logger.info(u"Adding attachments: {0}".format(unicode(attachment_list)))
            conn = self._get_rally_connection()
            conn.addAttachments(artifact, attachment_list_data)

mimetypes.add_type('text/plain', '.sql', strict=False)
