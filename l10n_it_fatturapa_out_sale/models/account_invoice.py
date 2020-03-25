#  Copyright 2020 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    fatturapa_sale_order_data = fields.Boolean(
        related='partner_id.fatturapa_sale_order_data'
    )
