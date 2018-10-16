# -*- coding: utf-8 -*-
# Copyright 2018 Sergio Corato (https://efatto.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
import re
import zipfile
import io
import os
import base64
from odoo import api, models
from odoo.tools import config

_logger = logging.getLogger(__name__)

FATTURAPA_IN_REGEX = "^[A-Z]{2}[a-zA-Z0-9]{11,16}_[a-zA-Z0-9]{,5}.(xml|zip)"
RESPONSE_MAIL_REGEX = '[A-Z]{2}[a-zA-Z0-9]{11,16}_[a-zA-Z0-9]{,5}_MT_' \
                      '[a-zA-Z0-9]{,3}'


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    @api.model
    def message_route(self, message, message_dict, model=None, thread_id=None,
                      custom_values=None):

        if any("@pec.fatturapa.it" in x for x in [
            message.get('Reply-To', ''),
            message.get('From', ''),
            message.get('Return-Path', '')
        ]):
            _logger.info("Processing FatturaPA PEC Invoice with Message-Id: "
                         "{}".format(message.get('Message-Id')))

            fatturapa_regex = re.compile(FATTURAPA_IN_REGEX)
            fatturapa_attachments = [x for x in message_dict['attachments']
                                     if fatturapa_regex.match(x.fname)]
            response_regex = re.compile(RESPONSE_MAIL_REGEX)
            response_attachments = [x for x in message_dict['attachments']
                                    if response_regex.match(x.fname)]
            if response_attachments and fatturapa_attachments:
                if len(response_attachments) > 1:
                    _logger.info(
                        'More than 1 message found in mail of incoming '
                        'invoice')
                message_dict['model'] = 'fatturapa.attachment.in'
                message_dict['record_name'] = message_dict['subject']
                message_dict['res_id'] = 0
                attachment_ids = self._message_post_process_attachments(
                    message_dict['attachments'], [], message_dict)
                for attachment in self.env['ir.attachment'].browse(
                        [att_id for model, att_id in attachment_ids]):
                    if fatturapa_regex.match(attachment.name):
                        self.create_fatturapa_attachment_in(attachment)

                message_dict['attachment_ids'] = attachment_ids
                del message_dict['attachments']
                del message_dict['cc']
                del message_dict['from']
                del message_dict['to']

                # model and res_id are only needed by
                # _message_post_process_attachments: we don't attach to
                del message_dict['model']
                del message_dict['res_id']

                # message_create_from_mail_mail to avoid to notify message
                # (see mail.message.create)
                self.env['mail.message'].with_context(
                    message_create_from_mail_mail=True).create(message_dict)
                _logger.info('Routing FatturaPA PEC E-Mail with Message-Id: {}'
                             .format(message.get('Message-Id')))
                return []

        return super(MailThread, self).message_route(
            message, message_dict, model=model, thread_id=thread_id,
            custom_values=custom_values)

    def create_fatturapa_attachment_in(self, attachment):
        decoded = base64.b64decode(attachment.datas)
        fatturapa_regex = re.compile(FATTURAPA_IN_REGEX)
        fatturapa_attachment_in = self.env['fatturapa.attachment.in']
        if attachment.mimetype == 'application/zip':
            with zipfile.ZipFile(io.BytesIO(decoded)) as zf:
                for file_name in zf.namelist():
                    inv_file = zf.open(file_name)
                    if fatturapa_regex.match(file_name):
                        # check if this invoice is already
                        # in other fatturapa.attachment.in
                        fatturapa_atts = fatturapa_attachment_in.search([
                            ('name', '=', file_name)])
                        if fatturapa_atts:
                            _logger.info("In invoice %s already processed"
                                         % fatturapa_atts.mapped('name'))
                        else:
                            fatturapa_attachment_in.create({
                                'name': file_name,
                                'datas_fname': file_name,
                                'datas': base64.encodestring(inv_file.read())})
        else:
            fatturapa_atts = fatturapa_attachment_in.search(
                [('name', '=', attachment.name)])
            if fatturapa_atts:
                _logger.info(
                    "Invoice xml already processed in %s"
                    % fatturapa_atts.mapped('name'))
            else:
                fatturapa_attachment_in.create({
                    'ir_attachment_id': attachment.id})
