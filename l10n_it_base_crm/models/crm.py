# -*- coding: utf-8 -*-
# Copyright 2013 Nicola Malcontenti - Agile Business Group
# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    province = fields.Many2one(comodel_name='res.province', string='Province')
    region = fields.Many2one(comodel_name='res.region', string='Region')

    @api.multi
    def _prepare_lead_contact(self):
        self.ensure_one()
        return {
            'province': self.province.id,
            'region': self.region.id,
        }

    @api.multi
    def _lead_create_contact(self, name, is_company, parent_id=False):
        self.ensure_one()
        partner_id = super(CrmLead, self) \
            ._lead_create_contact(name, is_company, parent_id=parent_id)
        if partner_id:
            partner_id.write(self._prepare_lead_contact())
        return partner_id
