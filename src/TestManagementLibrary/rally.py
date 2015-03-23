#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (c) 2015 Lingaro


import os
import base64

from pyral import Rally, RallyRESTAPIError
from robot.api import logger

class WrappedRally(Rally):
    """
    Wrapped Rally object to FIX some bugs.
    """

    def __init__(self, *args, **kwargs):
        self._project_provided = 'project' in kwargs
        super(WrappedRally, self).__init__(*args, **kwargs)

    def get(self, *args, **kwargs):
        if u'project' not in kwargs and not self._project_provided:
            kwargs['project'] = None
        return super(WrappedRally, self).get(*args, **kwargs)

    def _buildRequest(self, *args, **kwargs):
        result = super(WrappedRally, self)._buildRequest(*args, **kwargs)
        logger.info("url: " + result[2])
        return result

    def addAttachment(self, artifact, filename, mime_type='text/plain'):
        """
            Given an artifact (actual or FormattedID for an artifact), validate
            that it exists and then attempt to add an Attachment with the name and
            contents of filename into Rally and associate that Attachment
            with the Artifact.
            Upon the successful creation of the Attachment and linkage to the artifact,
            return an instance of the succesfully added Attachment.
            Exceptions are raised for other error conditions, such as the filename
            identified by the filename parm not existing, or not being a file, or the
            attachment file exceeding the maximum allowed size, or failure
            to create the AttachmentContent or Attachment.

        """
        # determine if artifact exists, if not short-circuit False
        # determine if attachment already exists for filename (with same size and content)
        #   if so, and already attached to artifact (or other entity), short-circuit True
        #   if so, but not attached to artifact (or other entity), save attachment
        #   if not, create the AttachmentContent with filename content,
        #           create the Attachment with basename for filename and ref the AttachmentContent
        #              and supply the ref for the artifact (or other object) in the Artifact field for Attachment
        #
        if not os.path.exists(filename):
            raise Exception('Named attachment filename: %s not found' % filename)
        if not os.path.isfile(filename):
            raise Exception('Named attachment filename: %s is not a regular file' % filename)

        attachment_file_name = os.path.basename(filename)
        attachment_file_size = os.path.getsize(filename)
        if attachment_file_size > self.MAX_ATTACHMENT_SIZE:
            raise Exception('Attachment file size too large, unable to attach to Rally Artifact')

        art_type, artifact = self._realizeArtifact(artifact)
        if not art_type:
            return False

        current_attachments = [att for att in artifact.Attachments]

        response = self.get('Attachment', fetch=True, query='Name = "%s"' % attachment_file_name)
        if response.resultCount:
            attachment = response.next()
            already_attached = [att for att in current_attachments if att.oid == attachment.oid]
            if already_attached:
                return already_attached[0]

        contents = ''
        # @WARN in original pyral method file was open in 'r' mode
        # it implicates that binary files was truncated on windows system (on linux system it works fine)
        with open(filename, 'rb') as af:
            file_content = af.read()
            contents = base64.b64encode(file_content)

        # create an AttachmentContent item
        ac = self.create('AttachmentContent', {"Content" : contents}, project=None)
        if not ac:
            raise RallyRESTAPIError('Unable to create AttachmentContent for %s' % attachment_file_name)

        attachment_info = { "Name"        :  attachment_file_name,
                            "Content"     :  ac.ref,       # ref to AttachmentContent
                            "ContentType" :  mime_type,
                            "Size"        :  attachment_file_size, # must be size before encoding!!
                            "User"        :  'user/%s' % self.contextHelper.user_oid,
                           #"Artifact"    :  artifact.ref  # (Artifact is an 'optional' field)
                          }
        # While it's actually possible to have an Attachment not linked to an Artifact,
        # in most cases, it'll be far more useful to have the linkage to an Artifact than not.
        # A special case is where the "Artifact" is actually a TestCaseResult, which is not a
        # subclass of Artifact in the Rally data model, but the WSAPI has been adjusted to permit
        # us to associate an Attachment with a TestCaseResult instance.
        if artifact:
            attachment_info["Artifact"] = artifact.ref
            if artifact._type == 'TestCaseResult':
                del attachment_info["Artifact"]
                attachment_info["TestCaseResult"] = artifact.ref
        # and finally, create the Attachment
        attachment = self.create('Attachment', attachment_info, project=None)
        if not attachment:
            raise RallyRESTAPIError('Unable to create Attachment for %s' % attachment_file_name)

        return attachment